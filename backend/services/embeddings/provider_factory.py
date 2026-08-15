from core.settings import settings


class EmbeddingProviderFactory:
    """
    Returns the configured embedding provider.
    """

    @staticmethod
    def create():
        provider = settings.EMBEDDING_PROVIDER.lower()

        if provider == "bge":
            from services.embeddings.bge_embedding_service import (
                BGEEmbeddingService,
            )

            return BGEEmbeddingService()

        raise ValueError(
            f"Unsupported embedding provider: {provider}"
        )