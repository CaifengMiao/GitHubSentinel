import schedule
import time
from github.client import GitHubClient
from notifier.email_notifier import EmailNotifier
from reporter.report_generator import ReportGenerator
from storage.database import Database
from config.settings import settings
from typing import List


class TaskScheduler:
    def __init__(self):
        self.github_client = GitHubClient()
        self.notifier = EmailNotifier()
        self.report_generator = ReportGenerator()
        self.database = Database()
        self.scheduled_jobs = []
        
    def check_repository_updates(self, owner: str, repo: str):
        """检查仓库更新并生成报告"""
        try:
            print(f"开始检查仓库更新: {owner}/{repo}")
            # 获取仓库事件
            events = self.github_client.get_repository_events(owner, repo)
            print(f"获取到 {len(events)} 个事件")
            
            # 保存事件到数据库
            for event in events:
                self.database.save_event(event)
            
            # 生成报告
            report = self.report_generator.generate_report(events)
            print("报告生成成功")
            print(f"报告内容:\n{report}")
            
            # 发送通知（忽略邮件通知错误）
            try:
                self.notifier.send_notification(report)
            except Exception as notify_error:
                print(f"发送通知时出错（已忽略）: {notify_error}")
            
        except Exception as e:
            print(f"检查仓库 {owner}/{repo} 更新时出错: {e}")
    
    def add_repository(self, owner: str, repo: str):
        """添加仓库到调度器"""
        # 根据配置设置调度间隔
        if settings.SCHEDULE_INTERVAL == "daily":
            job = schedule.every().day.do(self.check_repository_updates, owner, repo)
        elif settings.SCHEDULE_INTERVAL == "weekly":
            job = schedule.every().week.do(self.check_repository_updates, owner, repo)
        else:
            # 默认每天执行
            job = schedule.every().day.do(self.check_repository_updates, owner, repo)
        
        self.scheduled_jobs.append((owner, repo, job))
        print(f"已添加仓库到监控列表: {owner}/{repo}")
    
    def remove_repository(self, owner: str, repo: str):
        """从调度器移除仓库"""
        for scheduled_owner, scheduled_repo, job in self.scheduled_jobs:
            if scheduled_owner == owner and scheduled_repo == repo:
                schedule.cancel_job(job)
                self.scheduled_jobs.remove((scheduled_owner, scheduled_repo, job))
                print(f"已从监控列表移除仓库: {owner}/{repo}")
                return
        print(f"仓库不在监控列表中: {owner}/{repo}")
    
    def list_repositories(self):
        """列出所有监控的仓库"""
        return [(owner, repo) for owner, repo, _ in self.scheduled_jobs]
    
    def start_scheduler(self):
        """启动调度器"""
        # 运行调度器
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次