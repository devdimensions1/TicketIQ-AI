"""Thread-safe in-memory ticket store used by the demo UI.

Nothing is persisted: restarting the app clears all tickets.
"""
from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

STATUSES = ["Open", "In progress", "Resolved"]


@dataclass
class TicketRecord:
    ref: str
    created: datetime
    name: str
    email: str
    text: str
    category: str
    category_confidence: float
    priority: str
    sentiment: str
    sla: str
    escalate: bool
    suggested_reply: str
    related: List[str] = field(default_factory=list)
    status: str = "Open"


class TicketStore:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._items: Dict[str, TicketRecord] = {}

    def add(self, text: str, result, name: str = "", email: str = "",
            related: Optional[List[str]] = None) -> TicketRecord:
        with self._lock:
            ref = "TIQ-" + uuid.uuid4().hex[:6].upper()
            while ref in self._items:
                ref = "TIQ-" + uuid.uuid4().hex[:6].upper()
            rec = TicketRecord(
                ref=ref, created=datetime.now(), name=name.strip(), email=email.strip(),
                text=text.strip(), category=result.category,
                category_confidence=result.category_confidence, priority=result.priority,
                sentiment=result.sentiment, sla=result.sla, escalate=result.escalate,
                suggested_reply=result.suggested_reply, related=list(related or []),
            )
            self._items[ref] = rec
            return rec

    def get(self, ref: str) -> Optional[TicketRecord]:
        with self._lock:
            return self._items.get(ref.strip().upper())

    def all(self) -> List[TicketRecord]:
        """All tickets, newest first."""
        with self._lock:
            return sorted(self._items.values(), key=lambda r: r.created, reverse=True)

    def set_status(self, ref: str, status: str) -> bool:
        if status not in STATUSES:
            raise ValueError(f"Unknown status: {status}")
        with self._lock:
            rec = self._items.get(ref.strip().upper())
            if rec is None:
                return False
            rec.status = status
            return True

    def clear(self) -> None:
        with self._lock:
            self._items.clear()
