from __future__ import annotations

from sentence_transformers import SentenceTransformer


_model: SentenceTransformer | None = None


def embedding_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    return _model


def encode_texts(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []
    vectors = embedding_model().encode(texts, normalize_embeddings=True)
    return [v.tolist() for v in vectors]
