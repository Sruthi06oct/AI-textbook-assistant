# app.py
import os
from pathlib import Path
import streamlit as st
from rag_engine import RAGEngine
from utils import save_uploaded_file, pdf_to_text, MAX_PAGES

st.set_page_config(page_title="AI Teaching Assistant (Offline RAG)", layout="wide")
st.title("📚 AI Teaching Assistant – Offline RAG over Your Textbooks")
st.caption("No API key, no internet. TF-IDF based search & summaries 💛")

if "rag_engine" not in st.session_state:
    st.session_state.rag_engine = RAGEngine()
engine = st.session_state.rag_engine

st.sidebar.header("Upload Textbooks")
uploaded_pdfs = st.sidebar.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)

if uploaded_pdfs and st.sidebar.button("Index PDFs"):
    for pdf in uploaded_pdfs:
        path = save_uploaded_file(pdf)
        text = pdf_to_text(path)
        engine.index_pdf(text, Path(path).stem, pdf.name)
        st.sidebar.success(f"Indexed {pdf.name}")

indexed = engine.list_indexed_pdfs()

if indexed:
    titles = [b["title"] for b in indexed]
    ids = [b["pdf_id"] for b in indexed]

    choice = st.selectbox("Choose textbook", range(len(titles)), format_func=lambda i: titles[i])
    pdf_id = ids[choice]

    q = st.text_input("Ask a question")
    if st.button("Get Answer"):
        ans, status, cites = engine.answer_question(pdf_id, q)
        st.write(ans)
