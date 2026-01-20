#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = [
#     "mcp>=1.25.0",
#     "chromadb>=1.4.1",
#     "sentence-transformers>=5.2.0",
# ]
# ///
"""Claude Code Docs RAG MCP Server.

A single-file MCP server providing semantic search over Claude Code documentation.
Uses ChromaDB for vector storage and sentence-transformers for embeddings.
"""

import hashlib
import logging
import re
import sys
from pathlib import Path
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)

import chromadb
from chromadb.config import Settings
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from sentence_transformers import SentenceTransformer


# === Indexer ===


class DocsIndexer:
    """Indexes markdown docs and provides semantic search."""

    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    COLLECTION_NAME = "claude_code_docs"
    MAX_CHUNK_TOKENS = 1000  # ~4000 chars

    def __init__(self, docs_dir: Path, data_dir: Path):
        self.docs_dir = docs_dir
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self._model: Optional[SentenceTransformer] = None
        self._client: Optional[chromadb.PersistentClient] = None
        self._collection = None

    @property
    def model(self) -> SentenceTransformer:
        if self._model is None:
            self._model = SentenceTransformer(self.EMBEDDING_MODEL)
        return self._model

    @property
    def client(self) -> chromadb.PersistentClient:
        if self._client is None:
            self._client = chromadb.PersistentClient(
                path=str(self.data_dir / "chroma"),
                settings=Settings(anonymized_telemetry=False),
            )
        return self._client

    @property
    def collection(self):
        if self._collection is None:
            self._collection = self.client.get_or_create_collection(
                name=self.COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
            )
        return self._collection

    def is_indexed(self) -> bool:
        """Check if docs have been indexed."""
        return self.collection.count() > 0

    def list_topics(self) -> list[str]:
        """List all indexed documentation topics."""
        return [f.stem for f in self.docs_dir.glob("*.md")]

    def _chunk_document(self, content: str, filename: str) -> list[dict]:
        """Split document by headers, sub-chunk if needed."""
        chunks = []

        # Split by ## headers
        sections = re.split(r"\n(?=## )", content)

        for section in sections:
            if not section.strip():
                continue

            # Extract section title
            lines = section.strip().split("\n")
            title_match = re.match(r"^##\s*(.+)$", lines[0])
            section_title = title_match.group(1) if title_match else "Introduction"

            # If section is too long, sub-chunk by ### or by size
            section_text = section.strip()
            if len(section_text) > self.MAX_CHUNK_TOKENS * 4:
                # Sub-chunk by ### headers
                subsections = re.split(r"\n(?=### )", section_text)
                for i, subsec in enumerate(subsections):
                    if subsec.strip():
                        sub_title_match = re.match(
                            r"^###\s*(.+)$", subsec.split("\n")[0]
                        )
                        sub_title = (
                            sub_title_match.group(1)
                            if sub_title_match
                            else f"Part {i + 1}"
                        )
                        chunks.append(
                            {
                                "content": subsec.strip(),
                                "source": filename,
                                "section": f"{section_title} > {sub_title}",
                            }
                        )
            else:
                chunks.append(
                    {
                        "content": section_text,
                        "source": filename,
                        "section": section_title,
                    }
                )

        return chunks

    def reindex(self) -> int:
        """Re-index all documentation files."""
        logger.info("Starting reindex...")

        # Clear existing
        try:
            self.client.delete_collection(self.COLLECTION_NAME)
            logger.info("Cleared existing collection")
        except ValueError:
            logger.info("No existing collection to clear")
        self._collection = None

        # Chunk documents
        all_chunks = []
        md_files = list(self.docs_dir.glob("*.md"))
        logger.info(f"Found {len(md_files)} documentation files")

        for i, md_file in enumerate(md_files):
            content = md_file.read_text(encoding="utf-8")
            chunks = self._chunk_document(content, md_file.stem)
            all_chunks.extend(chunks)
            logger.info(f"[{i + 1}/{len(md_files)}] Chunked {md_file.stem}: {len(chunks)} chunks")

        if not all_chunks:
            logger.warning("No chunks to index")
            return 0

        logger.info(f"Total chunks: {len(all_chunks)}")

        # Generate embeddings
        logger.info("Generating embeddings (this may take a moment)...")
        texts = [c["content"] for c in all_chunks]
        embeddings = self.model.encode(texts, show_progress_bar=False).tolist()
        logger.info("Embeddings generated")

        # Generate IDs
        ids = [
            hashlib.md5(f"{c['source']}:{c['section']}:{i}".encode()).hexdigest()
            for i, c in enumerate(all_chunks)
        ]

        # Add to collection
        logger.info("Adding to ChromaDB collection...")
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=[
                {"source": c["source"], "section": c["section"]} for c in all_chunks
            ],
        )
        logger.info(f"Reindex complete: {len(all_chunks)} chunks indexed")

        return len(all_chunks)

    def search(self, query: str, limit: int = 5) -> list[dict]:
        """Semantic search across documentation."""
        if not self.is_indexed():
            return []

        query_embedding = self.model.encode([query], show_progress_bar=False).tolist()

        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=limit,
            include=["documents", "metadatas", "distances"],
        )

        output = []
        for i, doc in enumerate(results["documents"][0]):
            meta = results["metadatas"][0][i]
            distance = results["distances"][0][i]
            output.append(
                {
                    "content": doc,
                    "source": meta["source"],
                    "section": meta["section"],
                    "score": 1 - distance,  # Convert distance to similarity
                }
            )

        return output


# === MCP Server ===

mcp = FastMCP("claude_code_docs_mcp")

# Initialize indexer on startup
PLUGIN_ROOT = Path(__file__).parent
DOCS_DIR = PLUGIN_ROOT / "docs"
DATA_DIR = PLUGIN_ROOT / "data"
indexer = DocsIndexer(docs_dir=DOCS_DIR, data_dir=DATA_DIR)


class SearchInput(BaseModel):
    """Input for docs search."""

    query: str = Field(..., description="Search query", min_length=1)
    limit: int = Field(default=5, description="Max results", ge=1, le=20)


@mcp.tool(
    name="docs_search",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
    },
)
async def docs_search(params: SearchInput) -> str:
    """Search Claude Code documentation semantically.

    Returns relevant documentation chunks with source file and section info.
    Use this to find information about Claude Code features, configuration,
    hooks, MCP, skills, commands, and more.
    """
    results = indexer.search(params.query, params.limit)

    if not results:
        return f"No results found for: {params.query}"

    output = []
    for r in results:
        output.append(f"## {r['source']} - {r['section']}\n")
        output.append(f"Score: {r['score']:.3f}\n")
        output.append(f"{r['content']}\n")
        output.append("---\n")

    return "\n".join(output)


@mcp.tool(
    name="docs_list_topics",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
    },
)
async def docs_list_topics() -> str:
    """List all available Claude Code documentation topics."""
    topics = indexer.list_topics()
    return "\n".join(f"- {t}" for t in sorted(topics))


@mcp.tool(
    name="docs_reindex",
    annotations={
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
    },
)
async def docs_reindex() -> str:
    """Re-index all documentation. Run after docs are updated."""
    count = indexer.reindex()
    return f"Indexed {count} chunks from documentation."


if __name__ == "__main__":
    # Ensure index exists
    if not indexer.is_indexed():
        indexer.reindex()
    mcp.run()
