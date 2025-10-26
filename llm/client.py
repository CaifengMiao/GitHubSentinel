"""LLM 客户端模块，集成 OpenAI 和 DeepSeek API"""

import openai
from openai import OpenAI
from config.settings import settings


class LLMClient:
    def __init__(self):
        # 初始化可配置的 LLM 客户端
        self.client = OpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url=settings.LLM_BASE_URL
        )
        self.model = settings.LLM_MODEL
        self.system_prompt = settings.LLM_SYSTEM_PROMPT
        self.max_tokens = settings.LLM_MAX_TOKENS
        self.temperature = settings.LLM_TEMPERATURE
    
    def _complete(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"调用 LLM API 时出错: {e}")

    def generate_report_with_gpt4(self, prompt: str) -> str:
        """使用可配置的模型生成报告（兼容旧方法名）"""
        return self._complete(prompt)
    
    def generate_report_with_deepseek(self, prompt: str) -> str:
        """使用可配置的模型生成报告（兼容旧方法名）"""
        return self._complete(prompt)