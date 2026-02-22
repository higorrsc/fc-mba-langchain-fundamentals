"""
PGVector Similarity Search
--------------------------

Structured and production-ready similarity search example
using LangChain + PGVector + OpenAI embeddings.
"""

from __future__ import annotations

import os
from collections.abc import Iterable

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

# ==========================================================
# Configuration
# ==========================================================

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
# Vector Store Builder
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
        collection_name=os.environ["PGVECTOR_COLLECTION"],
        connection=os.environ["PGVECTOR_URL"],
        use_jsonb=True,
    )


# ==========================================================
# Search Logic
# ==========================================================


def similarity_search(
    store: PGVector,
    query: str,
    k: int = 3,
) -> list[tuple[Document, float]]:
    """
    Perform a similarity search on the vector store.

    Args:
        store: The PGVector instance to query.
        query: The search query string.
        k: Number of top similar results to retrieve.

    Returns:
        A list of tuples containing:
            - Document: The matched document.
            - float: The similarity score.
    """

    return store.similarity_search_with_score(query, k=k)


# ==========================================================
# Output Formatting
# ==========================================================


def print_results(results: list[tuple[Document, float]]) -> None:
    """Print similarity search results in a formatted and readable way."""

    if not results:
        print("No results found.")
        return

    for index, (doc, score) in enumerate(results, start=1):
        print("=" * 60)
        print(f"Result {index} | Score: {score:.4f}")
        print("=" * 60)

        print("\nContent:\n")
        print(doc.page_content.strip())

        if doc.metadata:
            print("\nMetadata:\n")
            for key, value in doc.metadata.items():
                print(f"{key}: {value}")

        print()


# ==========================================================
# Application Flow
# ==========================================================


def run_query(query: str, k: int = 3) -> None:
    """
    Execute the full similarity search workflow.

    This includes:
        - Building the vector store
        - Executing similarity search
        - Printing formatted results

    Args:
        query: The search query string.
        k: Number of top results to retrieve.
    """

    store = build_vector_store()
    results = similarity_search(store, query, k)
    print_results(results)


# ==========================================================
# Entrypoint
# ==========================================================


def main() -> None:
    """
    Application entry point.

    Loads environment variables, validates configuration,
    and executes a predefined similarity query.
    """
    load_dotenv()
    validate_env(REQUIRED_ENV_VARS)

    query = (
        "Tell me more about the gpt-5 thinking evaluation and performance "
        "results comparing to gpt-4"
    )

    run_query(query=query, k=3)


if __name__ == "__main__":
    main()
