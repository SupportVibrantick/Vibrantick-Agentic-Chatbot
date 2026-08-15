from __future__ import annotations

from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup
from docx import Document
from markdown import markdown
from pypdf import PdfReader

from models.knowledge_source import KnowledgeSourceType


class DocumentExtractor:
    """
    Extract plain text from supported document types.
    """

    async def extract(
        self,
        file_path: str,
        source_type: KnowledgeSourceType,
    ) -> str:
        """
        Dispatch extraction based on source type.
        """

        path = Path(file_path)

        match source_type:

            case KnowledgeSourceType.PDF:
                return self._extract_pdf(path)

            case KnowledgeSourceType.DOCX:
                return self._extract_docx(path)

            case KnowledgeSourceType.TXT:
                return self._extract_txt(path)

            case KnowledgeSourceType.CSV:
                return self._extract_csv(path)

            case KnowledgeSourceType.HTML:
                return self._extract_html(path)

            case KnowledgeSourceType.MARKDOWN:
                return self._extract_markdown(path)

            case _:
                raise ValueError(
                    f"Unsupported source type: {source_type}"
                )

    def _extract_pdf(
        self,
        path: Path,
    ) -> str:
        reader = PdfReader(path)

        pages = []

        for page in reader.pages:
            pages.append(page.extract_text() or "")

        return "\n".join(pages)

    def _extract_docx(
        self,
        path: Path,
    ) -> str:
        document = Document(path)

        return "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

    def _extract_txt(
        self,
        path: Path,
    ) -> str:
        return path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

    def _extract_csv(
        self,
        path: Path,
    ) -> str:
        dataframe = pd.read_csv(path)

        return dataframe.to_csv(index=False)

    def _extract_html(
        self,
        path: Path,
    ) -> str:
        html = path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        soup = BeautifulSoup(
            html,
            "html.parser",
        )

        return soup.get_text(
            separator="\n",
            strip=True,
        )

    def _extract_markdown(
        self,
        path: Path,
    ) -> str:
        md = path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        html = markdown(md)

        soup = BeautifulSoup(
            html,
            "html.parser",
        )

        return soup.get_text(
            separator="\n",
            strip=True,
        )