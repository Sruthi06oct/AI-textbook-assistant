# utils.py
import os
from PyPDF2 import PdfReader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")
INDEX_DIR = os.path.join(DATA_DIR, "index")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(INDEX_DIR, exist_ok=True)

MAX_PAGES = 30
TOP_K = 5
SIMILARITY_THRESHOLD = 0.08

def save_uploaded_file(uploaded_file):
    path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(path, "wb") as f:
        f.write(uploaded_file.read())
    return path

def pdf_to_text(path, max_pages=MAX_PAGES):
    reader = PdfReader(path)
    pages = []
    for i, p in enumerate(reader.pages):
        if i >= max_pages:
            break
        if p.extract_text():
            pages.append(p.extract_text())
    return "\n".join(pages)

def simple_sentence_split(text):
    out, cur = [], ""
    for c in text:
        cur += c
        if c in ".?!":
            out.append(cur.strip())
            cur = ""
    return outu