"""
Module 7 Project — Semantic Search Engine
==========================================
ingest.py — document loading, chunking, and ChromaDB storage

Run with:
    python ingest.py
    python ingest.py --chunk-size 200 --overlap 50
"""

import argparse
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer
import os

# CONFIGURATION
# Keep corpus, database, model, and chunking defaults in one place.
#____________________________________________________________________________
DOCS_DIR        = Path("docs")
CHROMA_PATH     = Path("chroma_data")
COLLECTION_NAME = "semantic_search"
MODEL_NAME      = "all-MiniLM-L6-v2"
DEFAULT_CHUNK_SIZE = 500
DEFAULT_OVERLAP    = 100


# LOAD SOURCE DOCUMENTS
# Preserve each file's full text and filename; chunking happens in a separate step.
#____________________________________________________________________________
def load_documents(
    directory: str,
    size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP
):
    """
    Load .txt and .md files from a directory.
    Args:
            directory:
                Folder containing the documents.
            size:
                Maximum number of characters per chunk.
            overlap:
                Number of characters shared between consecutive chunks.
    Returns:
        A list of dictionaries, one per source document.
    """
    documents = []
    
    for filename in os.listdir(directory):
        if filename.endswith(('.txt', '.md')):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            documents.append({
                "content": content,
                "source": filename,
            })
    return documents

# CHUNK DOCUMENT TEXT
# Overlapping windows keep nearby context available across chunk boundaries.
#________________________________________________________________________________
def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """
    Split text into fixed-size chunks with overlap.

    Args:
        text:       Full document text.
        chunk_size: Maximum characters per chunk.
        overlap:    Characters of overlap between consecutive chunks.

    Returns:
        List of non-empty chunk strings.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be between zero and chunk_size - 1")

    chunks = []
    start  = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end].strip())
        start += chunk_size - overlap # advance by a fixed step so this always terminates

    return [c for c in chunks if c] # Remove empty chunks


def get_collection(chroma_path: Path, collection_name: str):
    """Create (or retrieve) a persistent ChromaDB collection."""
    # Use persistent storage so indexed chunks remain available between runs.
    client = chromadb.PersistentClient(path=chroma_path)

    # Reuse the named collection when it exists; otherwise create it.
    collection = client.get_or_create_collection(
    name=collection_name,
    metadata={"description": "AI Engineering Educational Corpus"}
)

    print(f"Collection '{collection.name}' ready.")
    print(f"Current indexed chunk count: {collection.count()}")
    return collection



def ingest(chunk_size: int = DEFAULT_CHUNK_SIZE, overlap: int = DEFAULT_OVERLAP):
    """
    Full ingestion pipeline: load → chunk → embed → upsert.

    Each chunk is stored with metadata: source filename, chunk index,
    and the chunk size used — so experiments with different sizes can
    be compared without ambiguity.
    """
    documents = load_documents(str(DOCS_DIR))
    print(f"Source documents found: {len(documents)}")
    collection = get_collection(CHROMA_PATH, COLLECTION_NAME)

    # Keep text, metadata, and IDs in matching positions for the batch upsert.
    all_chunks = []
    all_metadatas = []
    all_ids = []

    for doc in documents:
        chunks = chunk_text(doc["content"], chunk_size, overlap)
        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            all_metadatas.append({
                "source": doc["source"],
                "chunk_index": str(i),
                "chunk_size": chunk_size,
            })
            all_ids.append(f"{doc['source']}_{i}")

    collection.upsert(
        documents=all_chunks,
        metadatas=all_metadatas,
        ids=all_ids
    )
    print(f"Successfully processed {len(all_chunks)} chunks")
    
    return len(all_chunks), len(documents), all_metadatas



# COMMAND-LINE ENTRY POINT
# Parse optional chunk settings, then run the same ingestion pipeline as imports.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Index docs/ into ChromaDB")
    parser.add_argument("--chunk-size", type=int, default=DEFAULT_CHUNK_SIZE)
    parser.add_argument("--overlap",    type=int, default=DEFAULT_OVERLAP)
    args = parser.parse_args()
    ingest(chunk_size=args.chunk_size, overlap=args.overlap)
