from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime


def parse_datetime(date_str: str) -> datetime:
    """解析GitHub返回的时间字符串"""
    return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")


@dataclass
class Repository:
    id: int
    name: str
    full_name: str
    owner: str
    description: Optional[str]
    url: str
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            id=data['id'],
            name=data['name'],
            full_name=data['full_name'],
            owner=data['owner']['login'],
            description=data.get('description'),
            url=data['html_url'],
            created_at=parse_datetime(data['created_at']),
            updated_at=parse_datetime(data['updated_at'])
        )


@dataclass
class Event:
    id: str
    type: str
    actor: str
    repo: str
    created_at: datetime
    payload: Dict
    
    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            id=data['id'],
            type=data['type'],
            actor=data['actor']['login'],
            repo=data['repo']['name'],
            created_at=parse_datetime(data['created_at']),
            payload=data.get('payload', {})
        )