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

4. 运行程序：
   ```bash
   python main.py
   ```

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

## 使用说明

1. 获取 GitHub Personal Access Token 并配置到 `.env` 文件
2. 配置邮件通知参数
3. 启动程序后，系统会根据配置的调度间隔定期检查仓库更新
4. 有更新时会通过邮件发送报告
5. 可以通过交互式命令行界面动态管理监控的仓库

## 贡献指南

欢迎提交 Issue 和 Pull Request。