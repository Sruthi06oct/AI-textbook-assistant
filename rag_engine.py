import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils import simple_sentence_split

# -------------------------------
# GOOGLE TOOL: Google Drive (Colab)
# -------------------------------
try:
    from google.colab import drive
    drive.mount('/content/drive')
    INDEX_DIR = "/content/drive/MyDrive/ai_teaching_assistant/index"
except:
    # Local fallback
    BASE = os.path.dirname(os.path.abspath(__file__))
    INDEX_DIR = os.path.join(BASE, "data", "index")

os.makedirs(INDEX_DIR, exist_ok=True)


class RAGEngine:
    def __init__(self):
        pass

    def _path(self, pdf_id):
        return os.path.join(INDEX_DIR, f"{pdf_id}.pkl")

    def index_pdf(self, text, pdf_id, title):
        chunks = [text[i:i+1000] for i in range(0, len(text), 850)]

        vectorizer = TfidfVectorizer(stop_words="english")
        vectors = vectorizer.fit_transform(chunks)

        data = {
            "title": title,
            "chunks": chunks,
            "vectorizer": vectorizer,
            "vectors": vectors
        }

        with open(self._path(pdf_id), "wb") as f:
            pickle.dump(data, f)

    def list_indexed_pdfs(self):
        books = []
        for file in os.listdir(INDEX_DIR):
            if file.endswith(".pkl"):
                with open(os.path.join(INDEX_DIR, file), "rb") as f:
                    data = pickle.load(f)
                books.append({
                    "pdf_id": file.replace(".pkl", ""),
                    "title": data.get("title", file.replace(".pkl", ""))
                })
        return books

    def answer_question(self, pdf_id, question, mode="short"):
        try:
            data = pickle.load(open(self._path(pdf_id), "rb"))
        except:
            return "PDF not indexed."

        vectorizer = data["vectorizer"]
        chunks = data["chunks"]
        vectors = data["vectors"]

        q_vec = vectorizer.transform([question])
        sims = cosine_similarity(q_vec, vectors).flatten()
        top_idx = sims.argsort()[::-1][:5]

        if sims[top_idx[0]] < 0.12:
            return f"No clear explanation of '{question}' found."

        good_sentences = []

        for idx in top_idx:
            for s in simple_sentence_split(chunks[idx]):
                s = s.strip()
                if len(s) < 25:
                    continue
                if ";" in s or "(" in s or ")" in s:
                    continue
                if any(char.isdigit() for char in s[:5]):
                    continue
                if any(k in s.lower() for k in [" is ", " are ", " where ", " contains ", " used "]):
                    good_sentences.append(s)

        if not good_sentences:
            return "Content exists, but no clear explanation found."

        sent_vecs = vectorizer.transform(good_sentences)
        sent_sims = cosine_similarity(q_vec, sent_vecs).flatten()
        order = sent_sims.argsort()[::-1]

        limit = 1 if mode == "short" else 3 if mode == "simple" else 5

        answer = []
        for i in order:
            if good_sentences[i] not in answer:
                answer.append(good_sentences[i])
            if len(answer) == limit:
                break

        return " ".join(answer)

    def summarize_book(self, pdf_id):
        data = pickle.load(open(self._path(pdf_id), "rb"))
        text = " ".join(data["chunks"])
        sentences = simple_sentence_split(text)
        return " ".join(sentences[:10])
