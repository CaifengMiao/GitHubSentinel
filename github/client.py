import requests
from config.settings import settings
from typing import List, Dict, Optional
from datetime import datetime
import os


class GitHubClient:
    def __init__(self):
        self.token = settings.GITHUB_TOKEN
        self.api_url = settings.GITHUB_API_URL
        # 当没有提供 Token 时，避免发送无效的 Authorization 头导致 401
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"
    
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

    def get_branches(self, owner: str, repo: str) -> List[str]:
        """获取仓库分支列表"""
        url = f"{self.api_url}/repos/{owner}/{repo}/branches"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            branches = response.json()
            return [b.get('name') for b in branches]
        else:
            response.raise_for_status()

    def get_commits(self, owner: str, repo: str, branch: Optional[str] = None,
                    since: Optional[str] = None, until: Optional[str] = None) -> List[Dict]:
        """获取提交记录，可按分支与时间范围过滤
        - branch: 分支名，映射到参数 `sha`
        - since/until: 时间范围，格式 "YYYY-MM-DDTHH:MM:SSZ"
        """
        url = f"{self.api_url}/repos/{owner}/{repo}/commits"
        params: Dict[str, str] = {}
        if branch:
            params["sha"] = branch
        if since:
            params["since"] = since
        if until:
            params["until"] = until
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
        issues = self.get_issues(owner, repo, state="all")
        pull_requests = self.get_pull_requests(owner, repo, state="all")
        
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

    def export_progress_by_date_range(self, owner: str, repo: str, days: int, branch: Optional[str] = None) -> str:
        """按时间范围导出进展到 Markdown 文件（过滤最近 days 天更新的 issue/PR）"""
        if days <= 0:
            days = 1
        now = datetime.utcnow()
        from datetime import timedelta
        threshold = now - timedelta(days=days)
    
        issues = self.get_issues(owner, repo, state="all")
        pull_requests = self.get_pull_requests(owner, repo, state="all")
    
        
        def parse_ts(s: str):
            try:
                # GitHub 时间格式示例: 2025-08-20T12:34:56Z
                from datetime import datetime as _dt
                return _dt.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
            except Exception:
                return now
    
        # 过滤最近 days 天更新的条目
        issues_filtered = [i for i in issues if parse_ts(i.get("updated_at", "1970-01-01T00:00:00Z")) >= threshold]
        prs_filtered = [p for p in pull_requests if parse_ts(p.get("updated_at", "1970-01-01T00:00:00Z")) >= threshold]
    
        start_date = threshold.strftime("%Y-%m-%d")
        end_date = now.strftime("%Y-%m-%d")
    
        content = f"# {owner}/{repo} - Progress ({start_date} ~ {end_date})\n\n"
        content += f"范围：最近 {days} 天（更新时间在 {start_date} 后）\n\n"
    
        content += "## Issues（最近更新）\n\n"
        for issue in issues_filtered:
            content += f"- **#{issue.get('number')}** {issue.get('title')}\n"
            content += f"  - State: {issue.get('state')}\n"
            content += f"  - Created: {issue.get('created_at')}\n"
            content += f"  - Updated: {issue.get('updated_at')}\n\n"
        if not issues_filtered:
            content += "- 无最近更新的 issues\n\n"
    
        content += "## Pull Requests（最近更新）\n\n"
        for pr in prs_filtered:
            content += f"- **#{pr.get('number')}** {pr.get('title')}\n"
            content += f"  - State: {pr.get('state')}\n"
            content += f"  - Created: {pr.get('created_at')}\n"
            content += f"  - Updated: {pr.get('updated_at')}\n\n"
        if not prs_filtered:
            content += "- 无最近更新的 pull requests\n\n"

        # Commits（按分支与时间范围）
        since_iso = threshold.strftime("%Y-%m-%dT%H:%M:%SZ")
        until_iso = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        try:
            repo_info = self.get_repository_info(owner, repo)
            default_branch = repo_info.get("default_branch") if isinstance(repo_info, dict) else None
        except Exception:
            default_branch = None
        branch_name = branch or default_branch
        commits = self.get_commits(owner, repo, branch=branch_name, since=since_iso, until=until_iso)

        content += "## Commits（最近提交）\n\n"
        if branch_name:
            content += f"分支：{branch_name}\n\n"
        if commits:
            import re
            types_count = {}
            breakings = []
            pr_refs = []
            for c in commits:
                sha = (c.get('sha') or '')[:7]
                commit_obj = c.get('commit') or {}
                msg = (commit_obj.get('message') or '').strip()
                author = (commit_obj.get('author') or {}).get('name') or 'Unknown'
                date = (commit_obj.get('author') or {}).get('date') or ''
                url = c.get('html_url') or ''

                m = re.match(r"^(?P<type>[a-zA-Z]+)(?:\((?P<scope>[^)]+)\))?(?P<bang>!)?:\s*(?P<subject>.+)", msg)
                type_ = None
                scope = None
                subject = msg
                is_breaking = False
                if m:
                    type_ = (m.group("type") or "").lower()
                    scope = m.group("scope")
                    subject = m.group("subject") or msg
                    is_breaking = bool(m.group("bang")) or ("BREAKING CHANGE" in msg)
                if type_:
                    types_count[type_] = types_count.get(type_, 0) + 1
                if is_breaking:
                    breakings.append(subject)
                pr_match = re.search(r"#(\d+)", msg)
                if pr_match:
                    pr_refs.append(pr_match.group(1))

                prefix = f"[{type_}{f'({scope})' if scope else ''}{'!' if is_breaking else ''}] " if type_ else ""
                content += f"- {prefix}{sha} {subject} — {author} ({date})\n"
                if url:
                    content += f"  - Link: {url}\n"

            # 概览与统计
            content += "\n### 提交概览\n"
            content += f"- 提交数量：{len(commits)}\n"
            if types_count:
                dist = ", ".join([f"{t}: {n}" for t, n in sorted(types_count.items(), key=lambda x: -x[1])])
                content += f"- 类型分布：{dist}\n"
            if pr_refs:
                uniq_prs = ", #".join(sorted(set(pr_refs), key=lambda x: int(x)))
                content += f"- 关联 PR：#{uniq_prs}\n"
            if breakings:
                content += f"- 重大变更：{len(breakings)} 条\n"
            content += "\n"
        else:
            content += "- 该时间范围内无提交\n\n"
    
        filename = f"{owner}_{repo}_{start_date}_to_{end_date}.md"
        output_dir = "daily_progress"
        import os
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
    
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
    
        return filepath