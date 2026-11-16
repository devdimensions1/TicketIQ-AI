"""Semantic-style similar ticket retrieval using TF-IDF cosine similarity."""
from __future__ import annotations

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SimilarTicketIndex:
    def __init__(self, corpus: list[dict]):
        self.corpus = corpus
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
        self.matrix = self.vectorizer.fit_transform([r["text"] for r in corpus])

    def query(self, text: str, k: int = 3) -> list[dict]:
        scores = cosine_similarity(self.vectorizer.transform([text]), self.matrix)[0]
        seen, results = set(), []
        for idx in scores.argsort()[::-1]:
            row = self.corpus[idx]
            key = row["text"]
            if key in seen:
                continue
            seen.add(key)
            results.append({"id": int(row["id"]), "text": row["text"], "category": row["category"],
                            "similarity": round(float(scores[idx]), 3)})
            if len(results) == k:
                break
        return results
