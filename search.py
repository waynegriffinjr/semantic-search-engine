"""
Module 7 Project — Semantic Search Engine
==========================================
search.py — query ChromaDB and return ranked results

Import this module into app.py:
    from search import search, get_collection_stats
"""

from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer
from ingest import get_collection, ingest

# ── Configuration (must match ingest.py) ─────────────────────────────────────
CHROMA_PATH     = Path("chroma_data")
COLLECTION_NAME = "semantic_search"
MODEL_NAME      = "all-MiniLM-L6-v2"


# def get_collection():
#     """Return the persistent ChromaDB collection."""
#     pass
collection = get_collection(CHROMA_PATH, COLLECTION_NAME)

def search(
    query: str,
    n_results: int = 5,
    sources: list[str] = None,
    distance_threshold: float = None,
) -> list[dict]:
    """
    Search the ChromaDB collection and return ranked results.

    Args:
        query:              Natural language search query.
        n_results:          Maximum number of results to return.
        sources:            If provided, only return chunks from these filenames.
        distance_threshold: If provided, exclude results with distance above this
                            value (lower = more similar).

    Returns:
        List of result dicts sorted by distance ascending (best first):
            {
                "text":        str,
                "source":      str,
                "chunk_index": int,
                "distance":    float,
                "score":       float,  # 1 - distance
            }
        Returns [] for empty queries or if the collection has no documents.
    """
    where = {"source": {"$in": sources}} if sources else None
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where      =where,
    )
    
    # Separate the ChromaDB returned fields for easier processing
    documents = results["documents"]
    metadatas = results["metadatas"]
    distances = results["distances"]
    
    # Stop if the query returned no result groups.
    if not documents or not metadatas or not distances:
        return []
    
    # One result group
    texts, metadata_rows, distance_rows = documents[0], metadatas[0], distances[0]
    # Stop if any of the result fields for this query are missing
    if texts is None or metadatas is None or distance_rows is None:
        return []
    
    matches = []
    # Prcoess each document alongside its metadata and distance
    for text, metadata, distance in zip(texts, metadata_rows, distance_rows):
        if metadata is None:
            continue
        
        # Exclude results at or above the maximum allowed distance
        if distance_threshold is not None and distance >= distance_threshold:
            continue
        
        # Keep the result fields and convert distance to a similarity score
        matches.append({
            "text"       : text,
            "source"     : metadata["source"],
            "chunk_index": metadata["chunk_index"],
            "distance"   : distance,
            "score"      : 1.0 - float(distance),
        })
        
        
    # Return the remaining results in ChromaDB's ranked order.        
    return matches


def get_collection_stats() -> dict:
    """
    Return basic stats about the indexed collection.

    Returns:
        {
            "total_chunks":   int,
            "unique_sources": int,
            "source_names":   list[str],
        }
    """
    # Store the three return values into variables used for stats
    dict_chunks, dict_sources, list_sources = ingest()
    
    # Extract the first occurrence source filename of unique chunks
    seen = set()
    unique_chunk_sources = []
    
    for chunk in list_sources:
        source = chunk.get("source")
        if source not in seen:
            seen.add(source)
            unique_chunk_sources.append(source)
    
    print({"total_chunks": dict_chunks, "unique_sources": dict_sources, "source_names": unique_chunk_sources})
    return {"total_chunks": dict_chunks, "unique_sources": dict_sources, "source_names": unique_chunk_sources}
