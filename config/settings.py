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
    
    # LLM 配置（抽取为可配置）
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.deepseek.com/v1")
    LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-chat")
    LLM_SYSTEM_PROMPT = os.getenv("LLM_SYSTEM_PROMPT", "You are a helpful assistant.")
    try:
        LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "1500"))
    except Exception:
        LLM_MAX_TOKENS = 1500
    try:
        LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    except Exception:
        LLM_TEMPERATURE = 0.7
    # 新增：LLM提供方（openai 兼容 / ollama）
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
    # Ollama 本地服务地址（仅在 provider=ollama 时使用）
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    # 提示词模板文件路径（JSON），可覆盖
    PROMPTS_PATH = os.getenv("PROMPTS_PATH", os.path.join(os.path.dirname(__file__), "prompts.json"))

settings = Settings()