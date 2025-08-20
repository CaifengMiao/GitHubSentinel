import requests
from config.settings import settings
from typing import List, Dict, Optional
from datetime import datetime
import os


class GitHubClient:
    def __init__(self):
        self.token = settings.GITHUB_TOKEN
        self.api_url = settings.GITHUB_API_URL
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def get_repository_events(self, owner: str, repo: str, 
                            event_types: Optional[List[str]] = None) -> List[Dict]:
        """获取仓库的最新事件"""
        url = f"{self.api_url}/repos/{owner}/{repo}/events"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            events = response.json()
            if event_types:
                events = [event for event in events if event.get('type') in event_types]
            return events
        else:
            response.raise_for_status()
    
    def get_repository_info(self, owner: str, repo: str) -> Dict:
        """获取仓库基本信息"""
        url = f"{self.api_url}/repos/{owner}/{repo}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
    
    def get_issues(self, owner: str, repo: str, state: str = "open") -> List[Dict]:
        """获取仓库的 issues 列表"""
        url = f"{self.api_url}/repos/{owner}/{repo}/issues"
        params = {"state": state}
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
    
    def get_pull_requests(self, owner: str, repo: str, state: str = "open") -> List[Dict]:
        """获取仓库的 pull requests 列表"""
        url = f"{self.api_url}/repos/{owner}/{repo}/pulls"
        params = {"state": state}
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
    
    def export_daily_progress(self, owner: str, repo: str, date: str = None) -> str:
        """导出每日进展到 Markdown 文件"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # 获取 issues 和 pull requests
        issues = self.get_issues(owner, repo)
        pull_requests = self.get_pull_requests(owner, repo)
        
        # 生成 Markdown 内容
        content = f"# {owner}/{repo} - Daily Progress ({date})\n\n"
        content += "## Issues\n\n"
        for issue in issues:
            content += f"- **#{issue['number']}** {issue['title']}\n"
            content += f"  - State: {issue['state']}\n"
            content += f"  - Created: {issue['created_at']}\n"
            content += f"  - Updated: {issue['updated_at']}\n\n"
        
        content += "## Pull Requests\n\n"
        for pr in pull_requests:
            content += f"- **#{pr['number']}** {pr['title']}\n"
            content += f"  - State: {pr['state']}\n"
            content += f"  - Created: {pr['created_at']}\n"
            content += f"  - Updated: {pr['updated_at']}\n\n"
        
        # 保存到文件
        filename = f"{owner}_{repo}_{date}.md"
        output_dir = "daily_progress"
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        return filepath