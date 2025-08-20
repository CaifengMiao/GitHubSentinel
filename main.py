from scheduler.tasks import TaskScheduler
from config.settings import settings
import threading
import time
import sys
import json
import os

def interactive_shell(scheduler: TaskScheduler):
    """交互式命令行界面"""
    print("GitHub Sentinel 交互式工具")
    print("可用命令:")
    print("  add <owner> <repo>    - 添加监控仓库")
    print("  remove <owner> <repo> - 移除监控仓库")
    print("  check <owner> <repo>  - 立即检查仓库更新")
    print("  list                 - 列出所有监控仓库")
    print("  quit                 - 退出程序")
    
    # 从配置文件读取初始仓库
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'repositories.json')
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            initial_repositories = json.load(f)
        for repo_info in initial_repositories:
            owner = repo_info['owner']
            repo = repo_info['repo']
            scheduler.add_repository(owner, repo)
            print(f"已添加仓库到监控列表: {owner}/{repo}")
    else:
        # 默认初始仓库
        initial_repositories = [
            {"owner": "microsoft", "repo": "vscode"},
            {"owner": "facebook", "repo": "react"},
        ]
        
        for repo_info in initial_repositories:
            owner = repo_info['owner']
            repo = repo_info['repo']
            scheduler.add_repository(owner, repo)
            print(f"已添加仓库到监控列表: {owner}/{repo}")
    
    while True:
        try:
            command = input("> ").strip().split()
            if not command:
                continue
                
            if command[0] == "quit":
                print("退出程序")
                break
            elif command[0] == "add" and len(command) == 3:
                scheduler.add_repository(command[1], command[2])
            elif command[0] == "remove" and len(command) == 3:
                scheduler.remove_repository(command[1], command[2])
            elif command[0] == "check" and len(command) == 3:
                owner = command[1]
                repo = command[2]
                # 验证仓库名称是否在配置文件中
                config_path = os.path.join(os.path.dirname(__file__), 'config', 'repositories.json')
                is_valid_repo = False
                if os.path.exists(config_path):
                    with open(config_path, 'r', encoding='utf-8') as f:
                        repositories = json.load(f)
                    for repo_info in repositories:
                        if repo_info['owner'] == owner and repo_info['repo'] == repo:
                            is_valid_repo = True
                            break
                
                if is_valid_repo:
                    print(f"立即检查仓库更新: {owner}/{repo}")
                    scheduler.check_repository_updates(owner, repo)
                else:
                    print(f"仓库 {owner}/{repo} 不在配置文件中，请检查仓库名称是否正确")
            elif command[0] == "list":
                repositories = scheduler.list_repositories()
                print("当前监控的仓库:")
                for owner, repo in repositories:
                    print(f"  {owner}/{repo}")
            else:
                print("未知命令或参数错误")
        except KeyboardInterrupt:
            print("\n退出程序")
            break
        except Exception as e:
            print(f"执行命令时出错: {e}")

def main():
    # 启动任务调度器
    scheduler = TaskScheduler()
    
    # 在后台线程运行调度器
    scheduler_thread = threading.Thread(target=scheduler.start_scheduler, daemon=True)
    scheduler_thread.start()
    
    # 启动交互式命令行界面
    interactive_shell(scheduler)

if __name__ == "__main__":
    main()