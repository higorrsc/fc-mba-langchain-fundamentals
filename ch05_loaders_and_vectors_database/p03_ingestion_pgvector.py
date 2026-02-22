"""
PDF → Chunk → Embeddings → PGVector Ingestion
---------------------------------------------

Refactored for:
- Clear separation of concerns
- Modern Python 3.13 typing
- Clean architecture style
"""

from __future__ import annotations

import os
from collections.abc import Iterable
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ==========================================================
# Configuration
# ==========================================================

PDF_FILENAME = "gpt5.pdf"
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"

REQUIRED_ENV_VARS: list[str] = [
    "OPENAI_API_KEY",
    "PGVECTOR_URL",
    "PGVECTOR_COLLECTION",
]


# ==========================================================
# Environment Validation
# ==========================================================


def validate_env(required_vars: Iterable[str]) -> None:
    """Ensure required environment variables are set and non-empty."""

    missing = [
        var
        for var in required_vars
        if not os.getenv(var) or not os.getenv(var, "").strip()
    ]

    if missing:
        formatted = ", ".join(missing)
        raise RuntimeError(f"Missing required environment variable(s): {formatted}")


# ==========================================================
# PDF Loading
# ==========================================================


def load_pdf(file_path: Path) -> list[Document]:
    """Load PDF file content"""

    if not file_path.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    return PyPDFLoader(str(file_path)).load()


# ==========================================================
# Text Splitting
# ==========================================================


def split_documents(documents: list[Document]) -> list[Document]:
    """Split documents into chunks."""

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        add_start_index=False,
    )

    splits = splitter.split_documents(documents)

    return [
        Document(
            page_content=doc.page_content,
            metadata={k: v for k, v in doc.metadata.items() if v not in ("", None)},
        )
        for doc in splits
    ]


# ==========================================================
# Vector Store
# ==========================================================


def build_vector_store() -> PGVector:
    """Create vector store from documents."""

    embeddings = OpenAIEmbeddings(
        model=os.getenv(
            "OPENAI_MODEL",
            DEFAULT_EMBEDDING_MODEL,
        )
    )

    return PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PGVECTOR_COLLECTION", ""),
        connection=os.getenv("PGVECTOR_URL", ""),
        use_jsonb=True,
    )


def generate_ids(count: int) -> list[str]:
    """Generate document IDs."""

    return [f"doc-{i}" for i in range(count)]


# ==========================================================
# Application Flow
# ==========================================================


def ingest_pdf() -> None:
    """Ingest PDF file into vector store."""

    script_dir = Path(__file__).resolve().parent
    pdf_path = script_dir / PDF_FILENAME

    documents = load_pdf(pdf_path)
    chunks = split_documents(documents)

    if not chunks:
        raise RuntimeError("No document chunks were generated.")

    store = build_vector_store()
    ids = generate_ids(len(chunks))

    store.add_documents(documents=chunks, ids=ids)

    print(f"Successfully indexed {len(chunks)} chunks.")


# ==========================================================
# Entrypoint
# ==========================================================


def main() -> None:
    """Main entrypoint for the application."""

    load_dotenv()
    validate_env(REQUIRED_ENV_VARS)
    ingest_pdf()


if __name__ == "__main__":
    main()
