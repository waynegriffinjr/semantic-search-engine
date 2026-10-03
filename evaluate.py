"""
Module 7 Project — Semantic Search Engine
==========================================
evaluate.py — precision and recall for your search system

Run with:
    python evaluate.py
    python evaluate.py --n-results 5 --threshold 0.4

Define your evaluation set in EVAL_SET, then run this script against
different index configurations (different chunk sizes) to compare results.
"""

import argparse
from search import search


# Define your evaluation set here.
# Each entry needs a query and the source filenames you expect to be relevant.
# Use at least 5 queries for the chunking experiment.
EVAL_SET = [
    # {"query": "...", "relevant_sources": ["filename.txt", ...]},
    {
      "query": "What is an AI hallucination?",
      "relevant_sources": ["llms-and-ai.txt"]  
    },
    {
      "query": "What makes Python a dynamic programming language?",
      "relevant_sources": ["python-advanced.txt", "python-fundamentals.txt", "streamlit.txt", "embeddings-and-vectors.txt", "fastapi.txt", "sql-databases.txt"]  
    },
    {
      "query": "How do I describe an API to a non-technical audience?",
      "relevant_sources": ["fastapi.txt", "rest-apis.txt","llms-and-ai.txt"]
    },
    {
      "query": "How do semantic searches work in AI Engineering?",
      "relevant_sources": ["embeddings-and-vectors.txt", "llms-and-ai.txt"]
    },
    {
      "query": "How to explain relational databases in a technical interview.",
      "relevant_sources": ["sql-databases.txt", "python-advanced.txt", "python-fundamentals.txt", "fastapi.txt"]
    }
]



def precision_recall(
    retrieved_sources: list[str], relevant_sources: list[str]
) -> tuple[float, float]:
    """
    Compute source-level precision and recall.

    Returns (precision, recall) as floats in [0, 1].
    """
    def precision_recall(
    retrieved_sources: list[str], relevant_sources: list[str]
) -> tuple[float, float]:
        """
        Compute source-level precision and recall.

        Returns (precision, recall) as floats in [0, 1].
        """
    retrieved = set(retrieved_sources)
    relevant = set(relevant_sources)
    correct = retrieved & relevant

    precision = (
        len(correct) / len(retrieved)
        if retrieved
        else 0.0
    )
    
    recall = (
        len(correct) / len(relevant)
        if relevant
        else 0.0
    )

    return precision, recall
    



def evaluate(n_results: int = 5, distance_threshold: float = None):
    """
    Run every query in EVAL_SET and print per-query and average precision/recall.
    """
    # Print the settings being used for this evaluation.
    print(
        f"\n=== Evaluation: "
        f"n_results={n_results}, "
        f"threshold={distance_threshold} ==="
        
    # Stop early if there are no queries; otherwise the averages below would
    # have no scores to divide by.
    if not EVAL_SET:
        print("No evaluation queries found.")
        return
            
    # Keep each query's scores so we can calculate an overall average afterward.
    precison_scores = []
    recall_scores   = []
    
    # Evaluate each query separately and number the output starting at 1
    # so it is easier to read.
    for index, entry in enumerate(EVAL_SET, start=1):
        query = entry["query"]
        relevant_sources = entry["relevant_sources"]
        
        # Search once for this query. Passing the threshold here lets search()
        # exclude results that are too dissimilar before they are scored.
         
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate search quality")
    parser.add_argument("--n-results", type=int,   default=5)
    parser.add_argument("--threshold", type=float, default=None)
    args = parser.parse_args()
    evaluate(n_results=args.n_results, distance_threshold=args.threshold)



