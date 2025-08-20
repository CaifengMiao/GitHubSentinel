import sqlite3
import json
from config.settings import settings
from typing import Dict, List


class Database:
    def __init__(self):
        self.db_path = settings.DATABASE_PATH
        self.init_database()
    
    def init_database(self):
        """初始化数据库表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建事件表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY,
                type TEXT,
                actor TEXT,
                repo TEXT,
                created_at TEXT,
                payload TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_event(self, event: Dict):
        """保存事件到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 检查事件是否已存在
        cursor.execute('SELECT id FROM events WHERE id = ?', (event['id'],))
        if cursor.fetchone():
            # 事件已存在，不需要重复保存
            conn.close()
            return
        
        # 插入新事件
        cursor.execute('''
            INSERT INTO events (id, type, actor, repo, created_at, payload)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            event['id'],
            event['type'],
            event['actor']['login'],
            event['repo']['name'],
            event['created_at'],
            json.dumps(event.get('payload', {}))
        ))
        
        conn.commit()
        conn.close()
    
    def get_events(self, limit: int = 100) -> List[Dict]:
        """获取最近的事件"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, type, actor, repo, created_at, payload
            FROM events
            ORDER BY created_at DESC
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        events = []
        for row in rows:
            event = {
                'id': row[0],
                'type': row[1],
                'actor': {'login': row[2]},
                'repo': {'name': row[3]},
                'created_at': row[4],
                'payload': json.loads(row[5])
            }
            events.append(event)
        
        return events