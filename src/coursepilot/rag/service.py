from coursepilot.exceptions import ValidationError
from coursepilot.llm.client import LLMClient
from coursepilot.models import RetrievedChunk
from coursepilot.rag.vector_store import VectorStore


class RAGService:
    def __init__(self, store: VectorStore, llm: LLMClient): self.store, self.llm = store, llm
    def answer(self, question: str) -> tuple[str, list[RetrievedChunk]]:
        chunks = self.store.search(question)
        if not chunks: raise ValidationError("资料库为空或没有找到相关内容。")
        context = "\n\n".join(f"[来源{i + 1}] {c.text}" for i, c in enumerate(chunks))
        answer = self.llm.answer(question, context)
        citations = "\n\n引用：" + "；".join(f"[{c.filename}｜{c.section}｜{'第'+str(c.location)+('页' if c.document_type == 'pdf' else '张')}]" for c in chunks)
        return answer.strip() + citations, chunks
