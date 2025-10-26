# GitHub Sentinel

一款开源工具类 AI Agent，专为开发者和项目管理人员设计，能够定期（每日/每周）自动获取并汇总订阅的 GitHub 仓库最新动态。

## 功能特性
- 订阅管理
- 更新获取
- 通知系统
- 报告生成
- 交互式命令行界面
- 每日进展模块
- LLM 集成
- 智能报告生成

## 技术架构

```text
GithubSentinel/
├── README.md
├── main.py
├── .env.example
├── config/
│   ├── __init__.py
│   └── settings.py
├── github/
│   ├── __init__.py
│   ├── client.py
│   └── models.py
├── scheduler/
│   ├── __init__.py
│   └── tasks.py
├── notifier/
│   ├── __init__.py
│   └── email_notifier.py
├── reporter/
│   ├── __init__.py
│   └── report_generator.py
├── storage/
│   ├── __init__.py
│   └── database.py
└── requirements.txt
```

## 模块说明

- **config**: 配置管理模块，负责读取环境变量和配置参数
- **github**: GitHub API 客户端模块，负责与 GitHub 进行交互
- **scheduler**: 任务调度模块，负责定期执行仓库更新检查
- **notifier**: 通知模块，负责发送仓库更新通知
- **reporter**: 报告生成模块，负责生成仓库更新汇总报告
- **storage**: 数据存储模块，负责保存和查询仓库事件数据
- **llm**: 大语言模型模块，负责调用 OpenAI 和 DeepSeek API
- **daily_progress**: 每日进展模块，负责导出仓库的每日进展到 Markdown 文件

## 安装与运行

1. 克隆项目：
   ```bash
   git clone <repository-url>
   cd GithubSentinel
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 配置环境变量：
   ```bash
   cp .env.example .env
   # 编辑 .env 文件填写 GitHub Token 等信息
   ```

4. 运行程序（命令行）：
   ```bash
   python main.py
   ```

5. 运行简洁版 UI（仅保留此客户端）：
   ```bash
   python ui/simple_app.py
   # 默认在 http://0.0.0.0:7860 提供服务
   ```
   - UI 输入：订阅下拉（来自 `config/repositories.json`）、报告周期滑块（天数）、模式单选（生成AI报告 / 查看历史报告）、历史报告下拉（按仓库与模式动态更新）
   - 模型选择：新增一级下拉选择 LLM 提供方（`DeepSeek` / `Ollama`）。当选择 `Ollama` 时在右侧显示二级模型下拉，选项直接来自本地 Ollama 模型官方标签（通过 `GET http://localhost:11434/api/tags` 动态加载，如 `deepseek-r1:8b`、`deepseek-r1:14b`）。
   - 提交按钮文案：生成AI报告模式显示“生成报告”，查看历史报告模式显示“查看报告”
   - 分支策略：自动使用仓库 `default_branch`，分支选择 UI 已移除
   - 右侧报告区：固定高度（约 77vh），内容在卡片内滚动；底部“报告导出”区域始终可见
   - AI 配置：支持 `DeepSeek` 远程 API 与 `Ollama` 本地推理。设置 `DEEPSEEK_API_KEY` 使用 DeepSeek；本地安装并运行 Ollama（默认 `http://127.0.0.1:11434`，可用 `OLLAMA_BASE_URL` 覆盖）。
   - 预览说明：IDE 内置预览可能报网络错误或 `NotOpenSSLWarning`（不影响功能），建议用系统浏览器访问

## 交互式命令行界面

程序启动后会进入交互式命令行界面，支持以下命令：

- `add <owner> <repo>`: 动态添加监控仓库
- `remove <owner> <repo>`: 动态移除监控仓库
- `check <owner> <repo>`: 立即检查指定仓库的更新
- `daily-report <owner> <repo>`: 生成指定仓库的每日报告
- `list`: 列出当前所有监控的仓库
- `quit`: 退出程序

调度器会在后台自动运行，按照配置的间隔定期检查仓库更新。

## 配置说明

在 `.env` 文件中配置以下参数：

- `GITHUB_TOKEN`: GitHub Personal Access Token
- `SCHEDULE_INTERVAL`: 调度间隔 (daily 或 weekly)
- `EMAIL_HOST`: 邮件服务器地址
- `EMAIL_PORT`: 邮件服务器端口
- `EMAIL_USER`: 邮件用户名
- `EMAIL_PASSWORD`: 邮件密码
- `EMAIL_RECIPIENTS`: 邮件收件人列表 (用逗号分隔)
- `DATABASE_PATH`: 数据库文件路径
- `DEEPSEEK_API_KEY`: DeepSeek API 密钥
- `OLLAMA_BASE_URL`: Ollama 服务地址（可选，默认 `http://127.0.0.1:11434`）

## 使用说明

1. 获取 GitHub Personal Access Token 并配置到 `.env` 文件
2. 配置邮件通知参数
3. 启动程序后，系统会根据配置的调度间隔定期检查仓库更新
4. 有更新时会通过邮件发送报告
5. 可以通过交互式命令行界面动态管理监控的仓库

## 最近更新

- UI 布局：右侧面板改为两行网格布局（`grid-template-rows: 1fr auto`），上行报告内容可滚动，下行导出区域固定显示。
- 报告卡片：卡片主体处理垂直滚动（`overflow-y: auto`），避免卡片随内容拉伸；下载区域默认高度保留，始终可见。
- 样式优化：移除卡片显式高度计算，统一使用弹性填充；右侧列固定高度约 77vh，溢出隐藏由卡片内容层接管。
- 交互改进：新增模式单选（生成AI报告 / 查看历史报告），历史报告下拉按仓库与模式动态更新。
- 提交按钮：根据模式动态切换文案（生成报告 / 查看报告）。
- 分支策略：自动使用仓库默认分支 `default_branch`；相关分支选择 UI 已移除以简化操作。
- 运行提示：IDE 内置预览可能显示 `net::ERR_ABORTED` 等网络错误，但不影响页面渲染；建议在系统浏览器中访问 `http://0.0.0.0:7860/`。
- 模型选择与联动：新增 LLM 提供方下拉（`DeepSeek` / `Ollama`），仅当选择 `Ollama` 时显示二级模型下拉；本地模型列表通过 `http://localhost:11434/api/tags` 动态获取并展示官方标签（如 `deepseek-r1:8b`、`deepseek-r1:14b`）。
- 模型默认与后端：优先默认 `deepseek-r1:14b`（若存在），生成报告时直接传递所选 Ollama 标签，不再做别名映射；非 Ollama 情况使用默认配置。
- 错误处理与提示：补充提示词模板缺失时的友好提示；IDE 预览的 OpenSSL/LibreSSL 警告不影响功能。

## 贡献指南

欢迎提交 Issue 和 Pull Request。