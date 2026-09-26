from uuid import uuid4

from coursepilot.exceptions import ValidationError
from coursepilot.llm.client import LLMClient
from coursepilot.models import QuizQuestion
from coursepilot.rag.vector_store import VectorStore


class QuizGenerator:
    def __init__(self, store: VectorStore, llm: LLMClient):
        self.store, self.llm = store, llm

    def generate(self, section: str) -> list[QuizQuestion]:
        chunks = self.store.search(section, limit=12, where={"section": section})
        if not chunks:
            raise ValidationError("所选章节没有可用于生成测验的资料。")
        payload = self.llm.quiz("\n\n".join(c.text for c in chunks))
        try:
            questions = [QuizQuestion(id=str(uuid4()), **item) for item in payload["questions"]]
        except Exception as exc:
            raise ValidationError("题目格式不正确，请重新生成。") from exc
        if len(questions) != 5 or sum(q.question_type == "multiple_choice" for q in questions) != 3:
            raise ValidationError("生成结果不符合 3 道单选和 2 道简答的要求，请重试。")
        return questions
