"""Training and loading of the TF-IDF + Logistic Regression classifiers."""
from __future__ import annotations

from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from .dataset import load_csv, write_csv

TARGETS = ("category", "priority", "sentiment")
MODEL_PATH = Path("models/ticketiq.joblib")
DATA_PATH = Path("data/tickets.csv")


def _pipeline() -> Pipeline:
    return Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True, stop_words="english")),
        ("clf", LogisticRegression(max_iter=1000, C=4.0)),
    ])


def train(data_path: Path = DATA_PATH, model_path: Path = MODEL_PATH) -> dict:
    """Train one classifier per target and persist them. Returns metrics."""
    if not Path(data_path).exists():
        write_csv(data_path)
    rows = load_csv(data_path)
    texts = [r["text"] for r in rows]
    bundle, metrics = {}, {}
    for target in TARGETS:
        labels = [r[target] for r in rows]
        x_tr, x_te, y_tr, y_te = train_test_split(texts, labels, test_size=0.2, random_state=7, stratify=labels)
        pipe = _pipeline().fit(x_tr, y_tr)
        metrics[target] = round(accuracy_score(y_te, pipe.predict(x_te)), 4)
        bundle[target] = _pipeline().fit(texts, labels)  # final model on all data
    bundle["corpus"] = rows
    Path(model_path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(bundle, model_path)
    return metrics


def load(model_path: Path = MODEL_PATH) -> dict:
    if not Path(model_path).exists():
        train(model_path=model_path)
    return joblib.load(model_path)


if __name__ == "__main__":
    for name, acc in train().items():
        print(f"{name:<10} accuracy: {acc:.1%}")
