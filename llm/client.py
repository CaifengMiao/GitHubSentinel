"""LLM 客户端模块，集成 OpenAI 兼容 API 与 Ollama"""

from openai import OpenAI
from typing import Optional
from config.settings import settings
import logging
import json
import requests

logger = logging.getLogger(__name__)


class LLMClient:
    def __init__(self, provider: Optional[str] = None, model: Optional[str] = None, base_url: Optional[str] = None):
        self.provider = (provider or settings.LLM_PROVIDER).strip().lower()
        # 规范化模型名：移除多余空格与包裹引号，避免因 .env 配置不当导致 400 "Model Not Exist"
        raw_model = model or settings.LLM_MODEL or "deepseek-chat"
        normalized_model = str(raw_model).strip().strip('"').strip("'")
        # 若使用 Ollama 且模型名存在空格且未包含冒号，尝试将空格替换为冒号以匹配常见标签格式（例如："qianwen 14b" -> "qianwen:14b"）
        if self.provider == "ollama":
            if (" " in normalized_model) and (":" not in normalized_model):
                normalized_model = normalized_model.replace(" ", ":")
        self.model = normalized_model
        # 修复：当 provider=ollama 时，优先使用 OLLAMA_BASE_URL 或显式传入的 base_url，避免误用 LLM_BASE_URL
        if self.provider == "ollama":
            self.base_url = (base_url or getattr(settings, "OLLAMA_BASE_URL", "http://localhost:11434")).rstrip("/")
        else:
            self.base_url = (base_url or getattr(settings, "LLM_BASE_URL", "")).rstrip("/")
        self.system_prompt = settings.LLM_SYSTEM_PROMPT
        self.max_tokens = settings.LLM_MAX_TOKENS
        self.temperature = settings.LLM_TEMPERATURE

        # 当使用 DeepSeek 端点时，且模型名非 deepseek-*，回退到默认 deepseek-chat，避免错误
        if self.provider != "ollama" and ("deepseek.com" in self.base_url) and not self.model.startswith("deepseek"):
            self.model = "deepseek-chat"

        if self.provider == "ollama":
            # Ollama 走本地 HTTP 接口，无需 OpenAI 客户端
            self.client = None
        else:
            # OpenAI 兼容（如 DeepSeek 等）
            self.client = OpenAI(
                api_key=settings.DEEPSEEK_API_KEY,
                base_url=self.base_url
            )
    
    def _complete(self, prompt: str) -> str:
        try:
            if self.provider == "ollama":
                # 使用 Ollama 本地接口
                endpoint = f"{self.base_url}/api/generate"
                payload = {
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    # 使用系统提示词增强一致性（旧版不支持则忽略）
                    "system": self.system_prompt or "",
                    # 参数映射：num_predict 对应 max_tokens
                    "options": {
                        "temperature": self.temperature,
                        "num_predict": self.max_tokens
                    }
                }
                try:
                    resp = requests.post(endpoint, json=payload, timeout=60)
                    resp.raise_for_status()
                    data = resp.json()
                    # 优先走 /api/generate 的返回结构
                    if isinstance(data, dict) and ("response" in data):
                        return data.get("response") or ""
                except requests.exceptions.HTTPError as http_err:
                    status = getattr(http_err.response, "status_code", None)
                    # 当路径不存在或方法不支持时，兜底改用 /api/chat
                    if status not in (404, 405):
                        raise
                # 兜底：尝试 /api/chat
                chat_endpoint = f"{self.base_url}/api/chat"
                chat_payload = {
                    "model": self.model,
                    "stream": False,
                    "messages": [
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    "options": {
                        "temperature": self.temperature,
                        "num_predict": self.max_tokens
                    }
                }
                resp2 = requests.post(chat_endpoint, json=chat_payload, timeout=60)
                resp2.raise_for_status()
                data2 = resp2.json()
                content = ""
                if isinstance(data2, dict):
                    msg = data2.get("message")
                    if isinstance(msg, dict):
                        content = msg.get("content") or ""
                return content
            else:
                # OpenAI 兼容客户端调用（DeepSeek 等）
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
                    # 若 DeepSeek 返回 Model Not Exist，则自动回退到 deepseek-chat 并重试一次
                    msg = str(e)
                    if ("deepseek.com" in self.base_url) and ("Model Not Exist" in msg or "invalid_request_error" in msg):
                        fallback_model = "deepseek-chat"
                        if self.model != fallback_model:
                            try:
                                logger.warning("DeepSeek 模型不可用：%s，回退为 %s 后重试", self.model, fallback_model)
                                self.model = fallback_model
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
                            except Exception:
                                # 重试仍失败则继续抛出原异常，由外层统一处理
                                pass
                    # 其他情况直接抛出，由外层包装错误信息
                    raise e
        except Exception as e:
            raise Exception(f"调用 LLM API 时出错: {e}")

    def generate_report_with_deepseek(self, prompt: str) -> str:
        """使用可配置的模型生成报告（兼容旧方法名）"""
        return self._complete(prompt)

    def generate_daily_report(self, markdown_content: str, dry_run: bool = False) -> str:
        """按示例风格提供统一入口：根据 provider 调用 deepseek 或 ollama。
        - 构造 messages: [system, user]
        - dry_run=True 时，将消息保存到 daily_progress/prompt.txt 并返回 "DRY RUN"
        - 返回生成的报告文本
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": markdown_content},
        ]

        if dry_run:
            logger.info("Dry run mode enabled. Saving prompt to file.")
            try:
                with open("daily_progress/prompt.txt", "w+", encoding="utf-8") as f:
                    json.dump(messages, f, indent=4, ensure_ascii=False)
            except Exception:
                # 仅记录，不影响 DRY RUN 返回
                logger.exception("保存 prompt 到文件失败")
            return "DRY RUN"

        if self.provider == "ollama":
            return self._generate_report_ollama(messages)
        else:
            # 默认走 OpenAI 兼容（用于 deepseek 等）
            return self._generate_report_deepseek(messages)

    def _generate_report_deepseek(self, messages: list) -> str:
        """使用 OpenAI 兼容客户端（deepseek）生成报告。"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"生成报告时发生错误（deepseek/openai 兼容）: {e}")
            raise

    def _generate_report_ollama(self, messages: list) -> str:
        """使用 Ollama 的 /api/chat 生成报告。"""
        try:
            endpoint = f"{self.base_url}/api/chat"
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens,
                },
            }
            resp = requests.post(endpoint, json=payload, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            content = ""
            if isinstance(data, dict):
                msg = data.get("message")
                if isinstance(msg, dict):
                    content = msg.get("content") or ""
            if not content:
                raise ValueError("Invalid response structure from Ollama API")
            return content
        except Exception as e:
            logger.error(f"生成报告时发生错误（ollama）: {e}")
            raise