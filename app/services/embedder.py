from app.config import embedding_model


def embed(text: str) -> list[float]:
    return embedding_model.encode(
        text,
        normalize_embeddings=True
    ).tolist()
