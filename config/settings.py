import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # GitHub API 配置
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GITHUB_API_URL = "https://api.github.com"
    
    # 调度配置
    SCHEDULE_INTERVAL = os.getenv("SCHEDULE_INTERVAL", "daily")  # daily 或 weekly
    
    # 通知配置
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    EMAIL_RECIPIENTS = os.getenv("EMAIL_RECIPIENTS", "").split(",")
    
    # 数据库配置
    DATABASE_PATH = os.getenv("DATABASE_PATH", "github_sentinel.db")
    
    # LLM 配置
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

settings = Settings()