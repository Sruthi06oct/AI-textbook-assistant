
import streamlit as st
from pathlib import Path
from rag_engine import RAGEngine
from utils import save_uploaded_file, pdf_to_text

st.set_page_config("AI Teaching Assistant", layout="wide")
st.title("📘 AI Teaching Assistant")

engine = RAGEngine()

uploaded_files = st.sidebar.file_uploader(
    "Upload PDF(s)", type=["pdf"], accept_multiple_files=True
)

if uploaded_files and st.sidebar.button("Index PDFs"):
    for file in uploaded_files:
        path = save_uploaded_file(file)
        text = pdf_to_text(path)
        engine.index_pdf(text, Path(path).stem, file.name)
        st.sidebar.success(f"Indexed {file.name}")

books = engine.list_indexed_pdfs()

if books:
    titles = [b["title"] for b in books]
    ids = [b["pdf_id"] for b in books]

    idx = st.selectbox("Select PDF", range(len(titles)),
                       format_func=lambda i: titles[i])
    pdf_id = ids[idx]

    question = st.text_input("Ask your question")
    mode = st.radio("Answer Type", ["Short", "Simple", "Detailed"])

    if st.button("Get Answer"):
        st.success(engine.answer_question(pdf_id, question, mode.lower()))

    if st.button("Summarize PDF"):
        st.text_area("Summary", engine.summarize_book(pdf_id), height=350)
