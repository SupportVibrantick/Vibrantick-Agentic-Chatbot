from __future__ import annotations

from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentChunker:
    """
    Splits extracted document text into chunks suitable
    for embedding and retrieval.
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                "",
            ],
        )

    async def chunk_text(
        self,
        text: str,
    ) -> list[str]:
        text = text.strip()

        if not text:
            return []

        return self.splitter.split_text(text)