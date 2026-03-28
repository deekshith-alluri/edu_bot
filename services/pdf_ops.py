import fitz  # PyMuPDF
import re
import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# -------- TEXT EXTRACTION --------
def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


# -------- PARAGRAPH SPLITTING --------
def split_into_paragraphs(text):
    chunks = re.split(r'\n\s*\n', text)
    return [c.strip() for c in chunks if len(c.strip()) > 50]


# -------- SMART PREVIEW (ENDS AT SENTENCE) --------
def smart_preview(text, limit=300):
    if len(text) <= limit:
        return text

    match = re.search(r'[.!?]', text[limit:])

    if match:
        end = limit + match.end()
        return text[:end]
    else:
        return text[:limit] + "..."


# -------- MAIN ENGINE --------
class PDFSearchEngine:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

        # Create cache folder if not exists
        os.makedirs("loaded_cache", exist_ok=True)

        # Generate cache file name based on PDF name
        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        self.cache_path = os.path.join("loaded_cache", f"{pdf_name}.pkl")

        if os.path.exists(self.cache_path):
            print("⚡ Loading cached index...")
            self.load()
        else:
            print("⏳ Building index...")
            self.build()
            self.save()

    def build(self):
        text = extract_text(self.pdf_path)
        self.chunks = split_into_paragraphs(text)

        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=15000
        )

        self.matrix = self.vectorizer.fit_transform(self.chunks)

    def save(self):
        with open(self.cache_path, "wb") as f:
            pickle.dump((self.chunks, self.vectorizer, self.matrix), f)

    def load(self):
        with open(self.cache_path, "rb") as f:
            self.chunks, self.vectorizer, self.matrix = pickle.load(f)

    def query(self, query, top_n=5):
        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.matrix).flatten()

        top_indices = scores.argsort()[-top_n:][::-1]

        results = [(self.chunks[i], scores[i]) for i in top_indices]
        return results


# -------- RUN --------
if __name__ == "__main__":
    pdf_path = "data/amulya_test.pdf"

    engine = PDFSearchEngine(pdf_path)

    while True:
        q = input("\nEnter query (or 'exit'): ")
        if q.lower() == "exit":
            break

        results = engine.query(q)

        print("\n🔍 Results:\n")
        for text, score in results:
            preview = smart_preview(text, 300)
            print(f"[{score:.4f}] {preview}\n")