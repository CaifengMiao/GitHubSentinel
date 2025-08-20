from scheduler.tasks import TaskScheduler
from config.settings import settings


def main():
    # 配置需要监控的仓库列表
    # 格式: (owner, repo)
    repositories = [
        ("microsoft", "vscode"),
        ("facebook", "react"),
        # 添加更多仓库...
    ]
    
    # 启动任务调度器
    scheduler = TaskScheduler()
    scheduler.start_scheduler(repositories)


if __name__ == "__main__":
    main()