# GitHub Sentinel 发布说明

## v0.3 (2024-05-21)

### 新增功能
- 将默认 LLM 从 GPT-4 更改为 DeepSeek
- 移除了对 OpenAI API 的依赖

### 配置更新
- 移除了 `OPENAI_API_KEY` 环境变量配置
- 保留了 `DEEPSEEK_API_KEY` 环境变量配置

### 依赖更新
- 移除了 `openai` 依赖包
- 保留了 `deepseek` 依赖包

### 使用说明
1. 更新 `.env` 文件，移除 `OPENAI_API_KEY` 配置项，确保 `DEEPSEEK_API_KEY` 已正确配置
2. 运行 `pip install -r requirements.txt` 安装更新后的依赖
3. 启动应用后，报告生成功能将默认使用 DeepSeek API

### 已知问题
- 暂无

## v0.2 (2024-05-20)

### 新增功能
- 每日进展跟踪模块：扩展了 GitHubClient，新增获取仓库每日 issues 和 pull requests 的功能，并将进展导出为 Markdown 文件
- LLM 模块：集成了 OpenAI 和 DeepSeek SDK，实现了调用 GPT-4 和 DeepSeek API 的功能
- 报告生成功能：实现了读取每日进展 Markdown 文件并调用 LLM API 生成正式项目每日报告的功能
- 交互式命令行界面扩展：添加了 `daily-report` 命令，支持手动生成指定仓库的每日报告
- 交互式命令行界面扩展：添加了 `daily-report-all` 命令，支持为所有监控仓库生成每日报告

### 改进功能
- 报告生成增强：优化了提示词，使生成的报告更具体、结构更清晰
- GitHub 客户端扩展：GitHubClient 现在支持获取仓库的每日 issues 和 pull requests
- 配置管理改进：在配置文件中添加了 LLM API 密钥的配置项
- 重复添加修复：修复了可以重复添加相同仓库的问题
- GitHub Token 修复：修复了 `.env` 文件中 GitHub Token 重复赋值导致的 401 认证错误

### 使用说明
1. 配置 `.env` 文件中的 `OPENAI_API_KEY` 和 `DEEPSEEK_API_KEY`
2. 使用 `add` 命令添加要监控的仓库
3. 使用 `check` 命令手动检查仓库更新
4. 使用 `daily-report` 命令手动生成每日报告
5. 使用 `daily-report-all` 命令为所有监控仓库生成每日报告
6. 使用 `list` 命令查看已添加的仓库
7. 使用 `remove` 命令移除不需要监控的仓库
8. 使用 `quit` 命令退出程序

### 已知问题
- 邮件通知功能默认是禁用的，需要在配置文件中启用
- 在某些情况下，GitHub API 的推送事件可能被拒绝

## v0.1 (2024-05-19)

### 初始版本功能
- GitHub 仓库监控：支持添加、移除和列出监控仓库
- 自动更新检查：定时任务自动检查仓库更新
- 邮件通知：通过邮件发送仓库更新通知
- SQLite 数据库存储：使用 SQLite 存储仓库信息和更新记录
- 交互式命令行界面：提供交互式命令行界面进行仓库管理

### 使用说明
1. 配置 `.env` 文件中的 GitHub Token 和邮件通知参数
2. 使用 `add` 命令添加要监控的仓库
3. 启动应用后，定时任务会自动检查仓库更新
4. 使用 `list` 命令查看已添加的仓库
5. 使用 `remove` 命令移除不需要监控的仓库
6. 使用 `quit` 命令退出程序

### 已知问题
- 邮件通知功能默认是禁用的，需要在配置文件中启用
- 在某些情况下，GitHub API 的推送事件可能被拒绝