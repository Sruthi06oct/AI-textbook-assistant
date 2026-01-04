# rag_engine.py
import os, pickle
import numpy as np
from typing import List, Dict, Any, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils import INDEX_DIR, simple_sentence_split, TOP_K, SIMILARITY_THRESHOLD

class RAGEngine:
    def _index_path(self, pdf_id):
        return os.path.join(INDEX_DIR, f"{pdf_id}.pkl")

    def _save_index(self, pdf_id, data):
        with open(self._index_path(pdf_id), "wb") as f:
            pickle.dump(data, f)

    def _load_index(self, pdf_id):
        with open(self._index_path(pdf_id), "rb") as f:
            return pickle.load(f)

    def list_indexed_pdfs(self):
        books = []
        for f in os.listdir(INDEX_DIR):
            if f.endswith(".pkl"):
                data = pickle.load(open(os.path.join(INDEX_DIR, f), "rb"))
                books.append({"pdf_id": f[:-4], "title": data["title"]})
        return books

    def index_pdf(self, text, pdf_id, title):
        chunks = [text[i:i+1000] for i in range(0, len(text), 850)]
        vec = TfidfVectorizer(stop_words="english")
        mat = vec.fit_transform(chunks)
        self._save_index(pdf_id, {"chunks": chunks, "vectorizer": vec, "chunk_vectors": mat, "title": title})

    def answer_question(self, pdf_id, question):
        data = self._load_index(pdf_id)
        vec = data["vectorizer"]
        qv = vec.transform([question])
        sims = cosine_similarity(qv, data["chunk_vectors"]).flatten()
        best = np.argmax(sims)

        if sims[best] < SIMILARITY_THRESHOLD:
            return "Not found in book.", "not_found", []

        sentences = simple_sentence_split(data["chunks"][best])
        return " ".join(sentences[:3]), "ok", []