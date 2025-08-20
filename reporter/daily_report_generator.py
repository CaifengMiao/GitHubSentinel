"""每日报告生成器，使用 LLM 整理汇总每日进展"""

import os
import markdown
from typing import List, Dict
from datetime import datetime
from llm.client import LLMClient


class DailyReportGenerator:
    def __init__(self):
        self.llm_client = LLMClient()
    
    def read_daily_progress_file(self, filepath: str) -> str:
        """读取每日进展 Markdown 文件"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    
    def generate_daily_report(self, owner: str, repo: str, date: str = None) -> str:
        """生成项目每日报告"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # 读取每日进展文件
        filename = f"{owner}_{repo}_{date}.md"
        filepath = os.path.join("daily_progress", filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"每日进展文件不存在: {filepath}")
        
        progress_content = self.read_daily_progress_file(filepath)
        
        # 构造提示词
        prompt = f"""你是一位专业的技术项目经理，负责为 {owner}/{repo} 项目编写每日进展报告。

项目信息:
- 项目名称: {owner}/{repo}
- 报告日期: {date}

原始进展数据:
{progress_content}

请根据以上数据生成一份结构化的每日报告，要求如下：

1. 报告标题: 项目名称 - 项目每日报告 (日期)
2. 概述: 用一段话总结今天的项目核心进展，突出重要更新。
3. Issues 更新:
   - 分类列出新增和更新的 issues
   - 对每个 issue 提供简要描述和链接
4. Pull Requests 更新:
   - 分类列出新增和更新的 pull requests
   - 对每个 PR 提供简要描述、作者和链接
5. 总结: 对今天的项目健康度进行评价，指出需要关注的问题或风险。

注意事项:
- 使用正式、专业的语言
- 突出关键信息，避免冗余
- 保持格式清晰、易读
- 不要添加原始数据中没有的信息
"""
        
        # 调用 DeepSeek API 生成报告
        report_content = self.llm_client.generate_report_with_deepseek(prompt)
        
        # 保存报告到文件
        report_filename = f"{owner}_{repo}_daily_report_{date}.md"
        report_dir = "daily_reports"
        os.makedirs(report_dir, exist_ok=True)
        report_filepath = os.path.join(report_dir, report_filename)
        
        with open(report_filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return report_filepath