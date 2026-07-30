import os
import streamlit as st
from app.pipeline.document_pipeline import DocumentPipeline
from app.embeddings.embedding_pipeline import EmbeddingPipeline
from app.vectorstore.qdrant_manager import QdrantManager
from app.pipeline.rag_pipeline import RAGPipeline

st.set_page_config(
    page_title="Adaptive Multi-Source RAG Framework",
    page_icon="📚",
    layout="wide"
)
document_pipeline = DocumentPipeline()
embedding_pipeline = EmbeddingPipeline()
qdrant_manager = QdrantManager()
rag_pipeline = RAGPipeline()
st.title("📚 Adaptive Multi-Source RAG Framework")

st.markdown("""
Upload one or more PDF documents, index them into the knowledge base,
and ask questions across all uploaded documents.
""")

st.divider()

# ==========================
# Upload Section
# ==========================

st.header("📄 Upload Documents")

uploaded_files = st.file_uploader(
    "Choose one or more PDF files",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:

    st.success(f"{len(uploaded_files)} document(s) selected.")

    st.write("### Selected Documents")

    for file in uploaded_files:
        st.write(f"📄 {file.name}")

    process_clicked = st.button(
        "🚀 Process Documents",
        use_container_width=True
    )

    if process_clicked:

        with st.spinner("Processing and indexing documents..."):
            os.makedirs("temp", exist_ok=True)

            qdrant_manager.reset_collection()

            total_chunks = 0
            total_vectors = 0

            for uploaded_file in uploaded_files:

                file_path = os.path.join(
                    "temp",
                    uploaded_file.name
                )

                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                document_chunks = document_pipeline.process(file_path)
                total_chunks += len(document_chunks)
                st.write(
                    f"✅ {uploaded_file.name}: {len(document_chunks)} chunks created."
                )
                embedded_chunks = embedding_pipeline.process_chunks(document_chunks)

                st.write(
                    f"🧠 {uploaded_file.name}: {len(embedded_chunks)} embeddings generated."
                )
                qdrant_manager.insert_chunks(embedded_chunks)

                st.write(
                    f"📦 {uploaded_file.name}: {len(embedded_chunks)} vectors indexed."
                )
                total_vectors += len(embedded_chunks)

        st.success(
            f"🎉 Successfully indexed {len(uploaded_files)} document(s)."
        )
        st.info(
            f"""
            **Summary**

            - Documents Indexed: **{len(uploaded_files)}**
            - Total Chunks: **{total_chunks}**
            - Total Vectors: **{total_vectors}**

            You can now ask questions across all uploaded documents.
            """
        )
        st.write(
            f"Vectors in Qdrant: {qdrant_manager.count_vectors()}"
        )
st.divider()

# ==========================
# Question Section
# ==========================

st.header("💬 Ask Questions")

question = st.text_input(
    "Enter your question"
)

ask_clicked = st.button(
    "Ask",
    use_container_width=True
)

st.divider()

# ==========================
# Placeholder
# ==========================

if ask_clicked:

    if question.strip():

        with st.spinner("Generating answer..."):

            result = rag_pipeline.answer_question(question)

        st.subheader("🤖 Answer")

        st.write(result["answer"])

        st.subheader("📚 Sources")

        if result["sources"]:

            for source in result["sources"]:
                st.markdown(
                    f"- **{source['document']}** (Page {source['page']})"
                )
        else:

            st.info("No relevant sources found.")

            
    else:

        st.warning("Please enter a question.")