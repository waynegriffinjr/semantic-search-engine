# Semantic Search Engine

## Overview

This is a semantic search tool built over a document collection. The tool loads, chunks,
embeds, and stores documents in ChromaDB, then provides a Streamlit interface
where users can type a question and see ranked results. You'll also run a
chunking experiment and document your findings.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Index the document corpus:
   ```bash
   python ingest.py
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```

## Files

| File | Purpose |
|------|---------|
| `app.py` | Streamlit search interface — your primary work file |
| `ingest.py` | Document loading, chunking, and ChromaDB storage |
| `search.py` | Search functions: query ChromaDB and rank results |
| `evaluate.py` | Evaluation framework: precision and recall |
| `docs/` | Starter document corpus (add your own documents here) |
| `chroma_data/` | Persistent ChromaDB storage (created on first run) |
| `requirements.txt` | Python dependencies |


## Chunking Experiment Results

source venv/bin/activate

python ingest.py --chunk-size 200 --overlap 50
python -c "from collections import Counter; from ingest import CHROMA_PATH, COLLECTION_NAME, get_collection; c=get_collection(CHROMA_PATH, COLLECTION_NAME); d=c.get(include=['metadatas']); print(Counter(m.get('chunk_size') for m in d['metadatas'] if m))"
python evaluate.py --n-results 5

python ingest.py --chunk-size 500 --overlap 50
python -c "from collections import Counter; from ingest import CHROMA_PATH, COLLECTION_NAME, get_collection; c=get_collection(CHROMA_PATH, COLLECTION_NAME); d=c.get(include=['metadatas']); print(Counter(m.get('chunk_size') for m in d['metadatas'] if m))"
python evaluate.py --n-results 5

**Chunk sizes tested:** _e.g. 200 chars vs 500 chars_

**Test queries:**
=== Evaluation: n_results=5, threshold=None ===
**Test queries:**
1. What is an AI hallucination?
2. What makes Python a dynamic programming language?
3. How do I describe an API to a non-technical audience?
4. How do semantic searches work in AI Engineering?
5. How to explain relational databases in a technical interview.


**Findings:**

_Which chunk size performed better overall, and why?_

chunk size = 500 (Avg. Precision: 86.667, Avg. Recall: 51.667)
chunk size = 200 (Avg. Precision: 76.667, Avg. Recall: 61.667)

With these five queries, 200-character chunks produced higher precision, while 500-character chunks produced higher recall. Smaller chunks may have made some results more focused, while larger chunks preserved more surrounding context. This is a tradeoff for this corpus and query set, not a general rule.