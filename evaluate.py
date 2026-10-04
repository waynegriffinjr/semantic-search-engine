"""
Semantic Search Engine
==========================================
evaluate.py — precision and recall for your search system

Run with:
    python evaluate.py
    python evaluate.py --n-results 5 --threshold 0.4
"""

import argparse
from search import search


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
    retrieved_sources: list[str], relevant_sources: list[str]) -> tuple[float, float]:
    """
    Compute source-level precision and recall.

    Returns (precision, recall) as floats in [0, 1].
    """
    # Store sets so each source file is counted once, even if search returned
    # multiple chunks from that file.
    retrieved = set(retrieved_sources)
    relevant = set(relevant_sources)

    # These are the source files that search returned and the evaluation
    # expected to find.
    correct = retrieved & relevant
    
    # Precision asks: "Of the files we retrieved, what fraction were relevant?"
    # If nothing was retrieved, return 0.0 instead of dividing by zero.
    precision = (
        len(correct) / len(retrieved)
        if retrieved
        else 0.0
    )
    # Recall asks: "Of the relevant files, what fraction did we retrieve?"
    # If no relevant files were listed, return 0.0 instead of dividing by zero.
    recall = (
        len(correct) / len(relevant)
        if relevant
        else 0.0
    )
    # Return precision first and recall second, as promised by the function.
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
    )
        
    # Stop early if there are no queries; otherwise the averages below would
    # have no scores to divide by.
    if not EVAL_SET:
        print("No evaluation queries found.")
        return
            
    # Keep each query's scores so we can calculate an overall average afterward.
    precision_scores = []
    recall_scores   = []
    
    # Evaluate each query separately and number the output starting at 1
    # so it is easier to read.
    for index, entry in enumerate(EVAL_SET, start=1):
        query = entry["query"]
        relevant_sources = entry["relevant_sources"]
        
        # Search once for this query. Passing the threshold here lets search()
        # exclude results that are too dissimilar before they are scored.
        results = search(
            query,
            n_results=n_results,
            distance_threshold=distance_threshold,
        )
        
        # Score at the source-file level rather than counting individual chunks.
        # Multiple returned chunks can come from the same source file.
        retrieved_sources = [result["source"] for result in results]
        
        # Compare the files search found with the files expected for this query.
        precision, recall = precision_recall(
            retrieved_sources,
            relevant_sources,
        )

        # Save the scores for the overall averages.
        precision_scores.append(precision)
        recall_scores.append(recall)
        
         # Print this query's scores to three decimal places for consistent,
        # easy-to-compare output.
        print(
            f"{index}. {query}\n"
            f"   Precision: {precision:.3f} | Recall: {recall:.3f}"
        )
        
    # Average query scores equally: each query contributes one precision and
    # one recall score, regardless of how many relevant files it has.
    average_precision = (sum(precision_scores) / len(precision_scores) * 100)
    average_recall    = (sum(recall_scores) / len(recall_scores) * 100)
    
    # Report the mean scores across the full evaluation set.
    print(
        f"\nAverage precision: {average_precision:.3f}"
        f" | Average recall: {average_recall:.3f }"
    )
    
    
def get_relevance_badge(distance):
    """
    Converts the ChromaDB distance into a relevance level.
    ChromaDB distance:
        Lower distance = more similar
        Higher distance = less similar
    Returns:
        A relevance label and a color for the badge.
    """
    if distance < 1.45:
        return "Highly Relevant", "green"
    elif distance < 1.55:
        return "Moderately Relevant", "orange"
    else:
        return "Low Relevance", "red"   

    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate search quality")
    parser.add_argument("--n-results", type=int,   default=5)
    parser.add_argument("--threshold", type=float, default=None)
    args = parser.parse_args()
    evaluate(n_results=args.n_results, distance_threshold=args.threshold)