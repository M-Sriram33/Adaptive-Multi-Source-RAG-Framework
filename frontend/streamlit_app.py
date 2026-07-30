import streamlit as st

st.set_page_config(
    page_title="Adaptive Multi-Source RAG Framework",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Adaptive Multi-Source RAG Framework")

st.markdown("""
### Review 1 - PDF Retrieval-Augmented Generation

Welcome to the baseline RAG system.

**Current Features**
- Upload PDF documents
- Ask questions from uploaded PDFs
- Display source citations (coming soon)
- Reject unrelated questions (coming soon)
""")

st.info("Project setup completed successfully. Ready to implement PDF ingestion.")