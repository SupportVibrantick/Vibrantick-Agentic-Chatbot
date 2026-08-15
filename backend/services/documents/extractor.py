from pathlib import Path

import pymupdf


class DocumentExtractionError(Exception):
    pass


class DocumentExtractor:

    async def extract_text(
        self,
        file_path: str,
    ) -> str:

        path = Path(file_path)

        if not path.exists():
            raise DocumentExtractionError(
                f"File not found: {file_path}"
            )

        if path.suffix.lower() != ".pdf":
            raise DocumentExtractionError(
                "Only PDF files are supported."
            )

        try:
            document = pymupdf.open(path)

            pages: list[str] = []

            for page_number in range(document.page_count):
                page = document.load_page(page_number)

                text = page.get_text("text")

                if text:
                    pages.append(text.strip())

            document.close()

            extracted_text = "\n\n".join(pages).strip()

            if not extracted_text:
                raise DocumentExtractionError(
                    "No text found in PDF."
                )

            return extracted_text

        except Exception as exc:
            raise DocumentExtractionError(
                f"Failed to extract PDF: {exc}"
            ) from exc