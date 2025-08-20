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
        
    def check_repository_updates(self, owner: str, repo: str):
        """检查仓库更新并生成报告"""
        try:
            # 获取仓库事件
            events = self.github_client.get_repository_events(owner, repo)
            
            # 保存事件到数据库
            for event in events:
                self.database.save_event(event)
            
            # 生成报告
            report = self.report_generator.generate_report(events)
            
            # 发送通知
            self.notifier.send_notification(report)
            
        except Exception as e:
            print(f"检查仓库 {owner}/{repo} 更新时出错: {e}")
    
    def start_scheduler(self, repositories: List[tuple]):
        """启动调度器"""
        # 根据配置设置调度间隔
        if settings.SCHEDULE_INTERVAL == "daily":
            for owner, repo in repositories:
                schedule.every().day.do(self.check_repository_updates, owner, repo)
        elif settings.SCHEDULE_INTERVAL == "weekly":
            for owner, repo in repositories:
                schedule.every().week.do(self.check_repository_updates, owner, repo)
        
        # 运行调度器
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次