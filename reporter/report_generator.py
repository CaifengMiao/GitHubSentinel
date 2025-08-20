from typing import List, Dict
from datetime import datetime


class ReportGenerator:
    def generate_report(self, events: List[Dict]) -> str:
        """生成仓库更新报告"""
        if not events:
            return "没有新的仓库更新。"
        
        # 按时间排序事件
        sorted_events = sorted(events, key=lambda x: x['created_at'], reverse=True)
        
        # 生成报告
        report_lines = ["GitHub Sentinel 仓库更新报告", "=" * 40, ""]
        
        for event in sorted_events:
            event_type = event.get('type', 'Unknown')
            actor = event.get('actor', {}).get('login', 'Unknown')
            repo = event.get('repo', {}).get('name', 'Unknown')
            created_at = event.get('created_at', 'Unknown')
            
            report_lines.append(f"- {event_type} 由 {actor} 在 {repo} ({created_at})")
        
        report_lines.extend(["", f"报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"])
        
        return "\n".join(report_lines)