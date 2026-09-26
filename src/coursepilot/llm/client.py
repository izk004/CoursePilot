import json
from openai import OpenAI
from coursepilot.config import Settings
from coursepilot.exceptions import LLMError
from coursepilot.llm.prompts import ANSWER_PROMPT, GRADE_PROMPT, QUIZ_PROMPT


class LLMClient:
    def __init__(self, settings: Settings): self.settings = settings
    def _complete(self, prompt: str) -> str:
        if not self.settings.llm_api_key:
            raise LLMError("请先在 .euv 配置 LLM_API_KEY。")
        try:
            client = OpenAI(
                api_key=self.settings.llm_api_key,
                base_url=self.settings.llm_base_url,
            )
            response = client.chat.completions.create(
                model=self.settings.llm_model,
                messages=[{"role":"user", "content": prompt}],
                temperature=0.2,
            )
            return response.choices[0].message.content or ""
        except Exception as exc: raise LLMError(f"LLM 请求失败：{exc}") from exc
    def answer(self, question: str, context: str) -> str: return self._complete(ANSWER_PROMPT.format(question=question, context=context))
    def quiz(self, context: str) -> dict: return self._json(QUIZ_PROMPT.format(context=context))
    def grade(self, prompt: str, reference: str, answer: str) -> dict: return self._json(GRADE_PROMPT.format(prompt=prompt, reference=reference, answer=answer))
    def _json(self, prompt: str) -> dict:
        raw = self._complete(prompt).strip().removeprefix("```json").removesuffix("```").strip()
        try: return json.loads(raw)
        except json.JSONDecodeError as exc: raise LLMError("LLM 返回的 JSON 无效，请重新生成。") from exc
