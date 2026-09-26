from typing import Any
import chromadb
from coursepilot.models import DocumentChunk, RetrievedChunk


class VectorStore:
    def __init__(self, path: str, embedding_function: Any):
        self.collection = chromadb.PersistentClient(path=path).get_or_create_collection(
            "course_materials", embedding_function=embedding_function, metadata={"hnsw:space": "cosine"})

    def add(self, chunks: list[DocumentChunk]) -> None:
        self.collection.upsert(ids=[c.id for c in chunks], documents=[c.text for c in chunks],
            metadatas=[c.model_dump(exclude={"id", "text"}) for c in chunks])

    def document_exists(self, document_id: str) -> bool:
        return bool(self.collection.get(where={"document_id": document_id}, limit=1)["ids"])

    def search(self, question: str, limit: int = 5, where: dict[str, Any] | None = None) -> list[RetrievedChunk]:
        available = self.collection.count()
        if available == 0:
            return []
        result = self.collection.query(
            query_texts=[question],
            n_results=min(limit, available),
            where=where,
            include=["documents", "metadatas", "distances"],
        )
        return [RetrievedChunk(id=result["ids"][0][i], text=result["documents"][0][i], distance=result["distances"][0][i], **result["metadatas"][0][i]) for i in range(len(result["ids"][0]))]

    def sections(self) -> list[str]:
        return sorted({m["section"] for m in self.collection.get(include=["metadatas"])["metadatas"]})
