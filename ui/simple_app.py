import os
import sys
from typing import List, Optional
from datetime import datetime

import gradio as gr

# 保证从 ui 子目录运行也能正确导入项目模块
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from github.client import GitHubClient
from llm.client import LLMClient
from config.settings import settings


def _format_size(num_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB"]
    size = float(num_bytes)
    for u in units:
        if size < 1024 or u == units[-1]:
            return f"{size:.2f} {u}"
        size /= 1024


def _make_download_link(md_text: str, filename: str) -> str:
    """生成可点击的 data URL 下载链接，避免使用 File 组件"""
    import base64
    data = base64.b64encode(md_text.encode("utf-8")).decode("ascii")
    href = f"data:text/markdown;base64,{data}"
    return f"<a href=\"{href}\" download=\"{filename}\">下载报告</a>"


def list_subscriptions() -> List[str]:
    """从配置文件读取订阅列表，返回 owner/repo 字符串列表"""
    config_path = os.path.join(PROJECT_ROOT, "config", "repositories.json")
    subs: List[str] = []
    if os.path.exists(config_path):
        import json
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for r in data:
            subs.append(f"{r['owner']}/{r['repo']}")
    return subs


def get_history_files(repo_full: Optional[str]) -> List[str]:
    """列出某个仓库在 daily_reports 下的历史报告文件名（basename）"""
    if not repo_full or "/" not in repo_full:
        return []
    owner, repo = repo_full.split("/", 1)
    report_dir = os.path.join(PROJECT_ROOT, "daily_reports")
    pattern = f"{owner}_{repo}_daily_report_*.md"
    import glob
    files = glob.glob(os.path.join(report_dir, pattern))
    files.sort()
    return [os.path.basename(p) for p in files]


github_client = GitHubClient()
llm_client = None


def export_progress_by_date_range(repo_full: str, days: int, mode: str, history_hint: Optional[str] = ""):
    """
    - mode == "生成AI报告": 导出最近 days 天进展，调用 AI 生成总结，保存并返回 (AI 报告, 大小+下载链接)
    - mode == "查看历史报告": 读取历史报告（按 hint 或最新），返回 (报告内容, 大小+下载链接)
    """
    if not repo_full or "/" not in repo_full:
        return "请选择有效的订阅项目 (owner/repo)", ""
    owner, repo = repo_full.split("/", 1)

    if mode == "查看历史报告":
        try:
            report_dir = os.path.join(PROJECT_ROOT, "daily_reports")
            pattern = f"{owner}_{repo}_daily_report_*.md"
            import glob
            candidates = glob.glob(os.path.join(report_dir, pattern))
            if history_hint:
                candidates = [p for p in candidates if history_hint in os.path.basename(p)] or candidates
            if not candidates:
                return "未找到历史报告", ""
            # 选择最新或第一个匹配
            candidates.sort()
            report_path = candidates[-1]
            with open(report_path, "r", encoding="utf-8") as f:
                content = f.read()
            size = os.path.getsize(report_path)
            size_str = _format_size(size)
            dl = _make_download_link(content, os.path.basename(report_path))
            info_md = f"报告大小：{size_str}\n\n" + dl
            return content, info_md
        except Exception as e:
            return f"读取历史报告出错: {e}", ""

    # 生成 AI 报告模式
    if not settings.DEEPSEEK_API_KEY:
        return "未配置 DEEPSEEK_API_KEY，无法使用AI生成报告。请在 .env 中设置。", ""

    try:
        # 1) 先导出最近 days 天的原始进展到文件
        raw_file_path = github_client.export_progress_by_date_range(owner, repo, days)
        with open(raw_file_path, "r", encoding="utf-8") as f:
            progress_md = f.read()

        # 2) 解析日期范围（文件名形如 owner_repo_YYYY-MM-DD_to_YYYY-MM-DD.md）
        base = os.path.basename(raw_file_path)
        prefix = f"{owner}_{repo}_"
        range_part = base[len(prefix):-3] if base.startswith(prefix) and base.endswith(".md") else ""
        start_date, end_date = ("", "")
        if "_to_" in range_part:
            parts = range_part.split("_to_")
            if len(parts) == 2:
                start_date, end_date = parts[0], parts[1]

        # 3) 构造 Prompt 并调用 LLM 生成总结报告
        global llm_client
        if llm_client is None:
            llm_client = LLMClient()
        prompt = f"""
你是一位专业的技术项目经理，负责为 {owner}/{repo} 项目编写进展总结报告（时间范围：{start_date} ~ {end_date}）。

原始进展数据（Issues、Pull Requests 与 Commits 最近更新）：
{progress_md}

请生成结构化的总结报告，要求：
1. 报告标题：项目名称 - 项目进展总结（{start_date} ~ {end_date}）
2. 概述：用一段话总结这段时间的核心进展与趋势。
3. Issues 更新：
   - 分类列出新增和更新的 issues（简要描述与链接，如可用）
4. Pull Requests 更新：
   - 分类列出新增和更新的 PR（简要描述、作者与链接，如可用）
5. 总结：对项目健康度进行评价，指出需要关注的问题或风险。

注意：使用正式、专业的语言；突出关键信息；不要添加原始数据中没有的内容。
"""
        ai_report_md = llm_client.generate_report_with_deepseek(prompt)

        # 4) 保存 AI 总结报告到 daily_reports
        report_dir = os.path.join(PROJECT_ROOT, "daily_reports")
        os.makedirs(report_dir, exist_ok=True)
        if start_date and end_date:
            report_filename = f"{owner}_{repo}_daily_report_{start_date}_to_{end_date}.md"
        else:
            today = datetime.now().strftime("%Y-%m-%d")
            report_filename = f"{owner}_{repo}_daily_report_{today}.md"
        report_path = os.path.join(report_dir, report_filename)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(ai_report_md)

        size = os.path.getsize(report_path)
        size_str = _format_size(size)
        dl = _make_download_link(ai_report_md, os.path.basename(report_path))
        info_md = f"报告大小：{size_str}\n\n" + dl
        return ai_report_md, info_md
    except Exception as e:
        return f"生成报告失败: {e}", ""


def _run_action(repo_full: str, days: int, mode: str, history_file: Optional[str]):
    """提交按钮处理：若选择了历史文件，则用其作为 hint 优先"""
    history_hint = history_file if (mode == "查看历史报告" and history_file) else ""
    return export_progress_by_date_range(repo_full, days, mode, history_hint)


def _update_history_dropdown(repo_full: Optional[str], mode: str):
    choices = get_history_files(repo_full) if mode == "查看历史报告" else []
    value = choices[-1] if choices else None
    return gr.update(choices=choices, value=value)


def _update_submit_label(mode: str):
    """根据模式更新提交按钮文案"""
    label = "生成报告" if mode == "生成AI报告" else "查看报告"
    return gr.update(value=label)




def _clear():
    # 清空左侧/右侧输出与历史选择
    return "", "", None


def _flag(repo_full: str, days: int, mode: str, history_file: Optional[str], report_md: str):
    try:
        import csv
        flagged_dir = os.path.join(PROJECT_ROOT, "flagged")
        os.makedirs(flagged_dir, exist_ok=True)
        log_path = os.path.join(flagged_dir, "log.csv")
        with open(log_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(timespec="seconds"),
                repo_full,
                days,
                mode,
                history_file or "",
                len(report_md or ""),
            ])
        return f"已标记到 {log_path}"
    except Exception as e:
        return f"标记失败：{e}"


subs = list_subscriptions()
with gr.Blocks(title="GitHubSentinel", css="""
#main-row { flex-wrap: nowrap; }
#main-row > .gr-column { min-width: 0; min-height: 0; }
.left-col, .right-col {
  /* 移除固定高度，使用自然高度避免按钮溢出到右侧 */
}
.left-col { display: flex; flex-direction: column; min-height: 0; overflow-y: auto; max-height: 80vh; }
.right-col { display: grid; grid-template-rows: 1fr auto; height: 77vh; min-height: 0; }
#left-actions { margin-top: auto; display: flex; justify-content: flex-start; gap: 8px; }

/* 价格卡片样式，用于右侧报告显示 */
.pricing-card {
     border: 1px solid #e5e7eb;
     border-radius: 12px;
     padding: 12px;
     background: inherit;
     display: flex;
     flex-direction: column;
      flex: 1 1 auto;
      min-height: 0;
      overflow: hidden; /* 防止子元素撑破，配合子元素滚动 */
   }
.pricing-card .card-header {
  font-weight: 600;
  font-size: 14px;
  margin-bottom: 8px;
}
.pricing-card .card-body {
  flex: 1 1 auto;
  overflow-y: auto;
  min-height: 0;
}
.pricing-card .card-body .prose {
  max-height: none;
  height: auto;
  min-height: 0;
}
/* 下载区紧贴卡片下方，且不随卡片滚动 */
.card-download { margin-top: 8px; flex: none; min-height: 56px; }
""") as demo:
    with gr.Row(elem_id="main-row"):
        with gr.Column(scale=1, elem_classes=["left-col"]):
            repo_dd = gr.Dropdown(choices=subs, value=(subs[0] if subs else None), label="订阅列表", info="已订阅GitHub项目")
            days_slider = gr.Slider(value=1, minimum=1, maximum=90, step=1, label="报告周期", info="生成项目过去一段时间进展，单位：天（含常用选项：14/30/60/90）")
            mode_radio = gr.Radio(choices=["生成AI报告", "查看历史报告"], value="生成AI报告", label="模式")
            history_files_dd = gr.Dropdown(choices=[], value=None, label="历史报告列表", info="按仓库自动列出历史报告以便选择")
            with gr.Row(elem_id="left-actions"):
                submit_btn = gr.Button("生成报告", variant="primary")
                clear_btn = gr.Button("清空")
                flag_btn = gr.Button("标记")
        with gr.Column(scale=1, elem_classes=["right-col"]):
            with gr.Group(elem_classes=["pricing-card"]):
                with gr.Column(elem_classes=["card-body"], scale=1):
                     out_md = gr.Markdown()
            info_html = gr.HTML(elem_classes=["card-download"]) 

    # 动态更新历史报告下拉
    repo_dd.change(_update_history_dropdown, inputs=[repo_dd, mode_radio], outputs=[history_files_dd])
    mode_radio.change(_update_history_dropdown, inputs=[repo_dd, mode_radio], outputs=[history_files_dd])
    mode_radio.change(_update_submit_label, inputs=[mode_radio], outputs=[submit_btn])

    submit_btn.click(
        _run_action,
        inputs=[repo_dd, days_slider, mode_radio, history_files_dd],
        outputs=[out_md, info_html],
    )

    clear_btn.click(
        _clear,
        inputs=[],
        outputs=[out_md, info_html, history_files_dd],
    )

    flag_btn.click(
        _flag,
        inputs=[repo_dd, days_slider, mode_radio, history_files_dd, out_md],
        outputs=[info_html],
    )

if __name__ == "__main__":
    demo.launch(share=True, server_name="0.0.0.0")