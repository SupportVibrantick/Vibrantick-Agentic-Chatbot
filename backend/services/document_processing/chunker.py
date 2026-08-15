from __future__ import annotations

import tiktoken


class DocumentChunker:
    """
    Splits extracted text into overlapping chunks.
    """

    def __init__(
        self,
        model: str = "text-embedding-3-small",
    ) -> None:
        self.encoding = tiktoken.encoding_for_model(model)

    def chunk(
        self,
        text: str,
        chunk_size: int,
        chunk_overlap: int,
    ) -> list[str]:
        """
        Split text into overlapping token chunks.
        """

        tokens = self.encoding.encode(text)

        chunks: list[str] = []

        start = 0

        while start < len(tokens):

            end = start + chunk_size

            chunk_tokens = tokens[start:end]

            chunks.append(
                self.encoding.decode(chunk_tokens)
            )

            if end >= len(tokens):
                break

            start = end - chunk_overlap

        return chunks