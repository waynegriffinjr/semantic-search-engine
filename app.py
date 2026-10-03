"""
Module 7 Project — Semantic Search Engine
==========================================
app.py — Streamlit search interface

Run with:
    streamlit run app.py

Make sure you've indexed documents first:
    python ingest.py
"""

import streamlit as st
from search import search, get_collection_stats
from ingest import DEFAULT_CHUNK_SIZE, DEFAULT_OVERLAP, injest


# STREAMLIT PAGE CONFIGURATION
#_______________________________________________________
st.set_page_config(
    page_title="Semantic Search Engine",
    page_icon="✨"
    layout-"wide"
)


# LOAD RESOURCES
#_______________________________________________________
@st.cache_resource
def load_resources():
     injest()


def get_relevance_badge(distance):
    """
    Converts the ChromaDB distance into a relevance level.
    ChromaDB distance:
        Lower distance = more similar
        Higher distance = less similar
    Returns:
        A relevance label and a color for the badge.
    """
    if distance < 0.5:
        return "Highly Relevant", "green"
    elif distance < 1:
        return "Moderately Relevant", "orange"
    else:
        return "Low Relevance", "red"   



# SIDEBAR — DOCUMENT MANAGEMENT
#_______________________________________________________
with st.sidebar:
    st.title("🗂️ Doucment Manager")
    
    if st.button("♺ Re-index Documents"):
        chunks = load_resources()
        st.write(f"Found {chunks} chunks")
        
        # Remove all exisiting chunks
        existing_ids = collection.get()["ids"]
        
        