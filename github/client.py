import requests
from config.settings import settings
from typing import List, Dict, Optional


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