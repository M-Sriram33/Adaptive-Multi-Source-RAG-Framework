import os
import streamlit as st

from app.pipeline.document_pipeline import DocumentPipeline
from app.embeddings.embedding_pipeline import EmbeddingPipeline
from app.vectorstore.qdrant_manager import QdrantManager

from app.sources.document_source import DocumentSource
from app.sources.sql.sql_source import SQLSource
from app.sources.api.api_source import APISource

from app.router.source_router import SourceRouter
from app.pipeline.multi_source_rag_pipeline import (
    MultiSourceRAGPipeline
)


st.set_page_config(
    page_title="Adaptive Multi-Source RAG Framework",
    page_icon="📚",
    layout="wide"
)
document_pipeline = DocumentPipeline()
embedding_pipeline = EmbeddingPipeline()
qdrant_manager = QdrantManager()


@st.cache_resource
def initialize_multi_source_pipeline():

    # Initialize all three sources
    document_source = DocumentSource()

    sql_source = SQLSource(
        database_path="data/sample_database/company.db"
    )

    api_source = APISource()

    # Register sources
    router = SourceRouter(
        sources=[
            document_source,
            sql_source,
            api_source
        ]
    )

    # Initialize complete RAG pipeline
    pipeline = MultiSourceRAGPipeline(
        router=router
    )

    return pipeline


multi_source_pipeline = initialize_multi_source_pipeline()
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

st.divider()

st.header("💬 Ask Questions Across Multiple Sources")

question = st.text_area(
    "Enter your question",
    placeholder=(
        "Example:employee salary information, AAPL stock price."
    ),
    height=100
)

ask_clicked = st.button(
    "🚀 Generate Answer",
    use_container_width=True,
    type="primary"
)

if ask_clicked:

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        try:
            with st.spinner(
                "Retrieving information from relevant sources "
                "and generating your answer..."
            ):

                result = multi_source_pipeline.answer_question(
                    question
                )

            # Display generated answer
            st.subheader("🤖 Generated Answer")
            st.markdown(result["answer"])

            st.divider()

            # Display selected sources
            st.subheader("🔍 Sources Used")

            sources_used = result.get("sources_used", [])

            if sources_used:
                cols = st.columns(len(sources_used))

                for col, source_name in zip(cols, sources_used):
                    with col:
                        st.success(source_name.upper())

            # Display source references
            st.subheader("📚 Source References")

            sources = result.get("sources", [])

            if sources:

                for index, source in enumerate(sources, start=1):

                    with st.expander(
                        f"Source {index}: "
                        f"{source.get('source_type', 'Unknown').upper()}"
                    ):

                        st.json(source)

            else:
                st.info("No source references available.")

        except Exception as error:

            st.error(
                f"An error occurred while generating the answer: {error}"
            )
