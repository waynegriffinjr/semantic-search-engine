"""
Semantic Search Engine
==========================================
app.py — Streamlit search interface

Run with:
    streamlit run app.py

Make sure you've indexed documents first:
    python ingest.py
"""

import streamlit as st
from search import search, get_collection_stats
from ingest import (
    CHROMA_PATH,
    COLLECTION_NAME,
    DEFAULT_CHUNK_SIZE,
    DEFAULT_OVERLAP,
    ingest,
    get_collection,
)
from evaluate import get_relevance_badge


# STREAMLIT PAGE CONFIGURATION
#_______________________________________________________
st.set_page_config(
    page_title="Semantic Search Engine",
    page_icon="✨",
    layout="wide",
)

# st.markdown(
#     """
#     <style>
#     /* Main page */
#     .stApp,
#     [data-testid="stMain"] {
#         background-color: #ffffff;
#         color: #111111;
#     }

#     [data-testid="stMain"] * {
#         color: #111111;
#     }

#     /* Main title only; sidebar title stays white */
#     [data-testid="stMain"] h1 {
#         color: #c62828 !important;
#     }

#     /* Sidebar */
#     [data-testid="stSidebar"] {
#         background-color: #111111;
#     }

#     [data-testid="stSidebar"] * {
#         color: #ffffff !important;
#     }

#     /* Inputs and select controls */
#     [data-testid="stTextInput"] input,
#     [data-baseweb="select"] {
#         border: 1px solid #111111 !important;
#         border-radius: 4px;
#     }

#     /* Buttons */
#     .stButton > button,
#     [data-testid="stFormSubmitButton"] button {
#         border: 1px solid #111111;
#         border-radius: 4px;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# LOAD RESOURCES
#_______________________________________________________
@st.cache_resource
def load_resources():
    return get_collection(CHROMA_PATH, COLLECTION_NAME)

collection = load_resources()


# SIDEBAR — DOCUMENT MANAGEMENT
#_______________________________________________________
with st.sidebar:
    st.title("🗂️ Document Manager")
    
    if st.button("♺ Prepare Documents"):
        with st.spinner("Indexing documents... Please wait"):
            chunks, docs, metadatas  = ingest(
                chunk_size=DEFAULT_CHUNK_SIZE,
                overlap=DEFAULT_OVERLAP,
        )
        st.success(f"Indexed {chunks} chunks from {docs} documents.")
    
        
    n_results = st.slider(
        "Nummber of results",
        min_value=1,
        max_value=20,
        value=5,
    )
    
    source_names = [
    "python-advanced.txt",
    "python-fundamentals.txt",
    "streamlit.txt",
    "embeddings-and-vectors.txt",
    "fastapi.txt",
    "sql-databases.txt",
    "llms-and-ai.txt",
    "rest-apis.txt",
]
    
    selected_sources = st.multiselect(
        "Filter Source Documents",
        options=source_names,
    )
        
# SEARCH BAR
#_______________________________________________________________________________
st.title("✨Semantic Search Engine")


with st.form(key="search_form"):
    search_query = st.text_input(
        label="Search Query",
        placeholder="Ask anything about the internal documents...", 
        
    )
    submit_button = st.form_submit_button(label="Search")
    
if submit_button and search_query.strip():
    results = search(
        search_query, 
        n_results=n_results,
        sources=selected_sources,
    )
    
    st.write(f"Form submitted! Fetching results for: {search_query}")
    st.metric("Results returned", len(results))
    
    
    if not results:
        st.info("No results found.")
        
    for result in results:
        st.write(result["text"])
        
        
        label, color = get_relevance_badge(result["distance"])

        st.markdown(
            f'<span style="background-color: {color}; color: white; '
            f'padding: 4px 8px; border-radius: 4px;">{label}</span>',
            unsafe_allow_html=True,
        )
        
        
        st.caption(
            f"Source: {result['source']} | Relevance: {result['score']:.3f}"
        )
        
        
    
    


        
        