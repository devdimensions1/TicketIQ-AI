"""High-level triage engine combining classifiers, search and replies."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field

from . import models
from .replies import sla_for, suggest_reply
from .search import SimilarTicketIndex


@dataclass
class TriageResult:
    category: str
    category_confidence: float
    priority: str
    sentiment: str
    sla: str
    escalate: bool
    suggested_reply: str
    similar_tickets: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


class TriageEngine:
    def __init__(self):
        bundle = models.load()
        self._clf = {t: bundle[t] for t in models.TARGETS}
        self._index = SimilarTicketIndex(bundle["corpus"])

    def triage(self, text: str, k: int = 3) -> TriageResult:
        if not text or not text.strip():
            raise ValueError("Ticket text must not be empty")
        category = self._clf["category"].predict([text])[0]
        confidence = float(self._clf["category"].predict_proba([text]).max())
        priority = self._clf["priority"].predict([text])[0]
        sentiment = self._clf["sentiment"].predict([text])[0]
        return TriageResult(
            category=category,
            category_confidence=round(confidence, 3),
            priority=priority,
            sentiment=sentiment,
            sla=sla_for(priority),
            escalate=priority == "high" and sentiment == "negative",
            suggested_reply=suggest_reply(category, priority, sentiment),
            similar_tickets=self._index.query(text, k),
        )
