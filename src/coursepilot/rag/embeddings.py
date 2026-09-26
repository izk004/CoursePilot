from sentence_transformers import SentenceTransformer


class LocalEmbeddingFunction:
    def __init__(self, model_name: str): self.model = SentenceTransformer(model_name)
    def __call__(self, input: list[str]) -> list[list[float]]:
        return self.model.encode(input, normalize_embeddings=True).tolist()
    def name(self) -> str: return "coursepilot-local-embeddings"
