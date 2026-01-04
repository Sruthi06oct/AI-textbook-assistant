# utils.py
import os
from PyPDF2 import PdfReader

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")
UPLOAD_DIR = os.path.join(DATA, "uploads")

os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_uploaded_file(file):
    path = os.path.join(UPLOAD_DIR, file.name)
    with open(path, "wb") as f:
        f.write(file.read())
    return path

def pdf_to_text(path, max_pages=30):
    reader = PdfReader(path)
    text = []
    for i, page in enumerate(reader.pages):
        if i >= max_pages:
            break
        if page.extract_text():
            text.append(page.extract_text())
    return "\n".join(text)

def simple_sentence_split(text):
    sentences, current = [], ""
    for c in text:
        current += c
        if c in ".?!":
            sentences.append(current.strip())
            current = ""
    return sentences
