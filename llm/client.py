"""LLM 客户端模块，集成 OpenAI 和 DeepSeek API"""

import openai
from openai import OpenAI
from config.settings import settings


class LLMClient:
    def __init__(self):
        # 初始化 DeepSeek 客户端
        # DeepSeek API 与 OpenAI API 兼容，只需更改 base_url
        self.deepseek_client = OpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com/v1"
        )
    
    def generate_report_with_gpt4(self, prompt: str) -> str:
        """使用 DeepSeek 生成报告"""
        try:
            response = self.deepseek_client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"调用 DeepSeek API 时出错: {e}")
    
    def generate_report_with_deepseek(self, prompt: str) -> str:
        """使用 DeepSeek 生成报告"""
        try:
            response = self.deepseek_client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"调用 DeepSeek API 时出错: {e}")