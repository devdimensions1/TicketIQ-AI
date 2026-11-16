"""Thread-safe ticket store backed by SQLite.

``TicketStore()`` is in-memory (used by tests). ``TicketStore("data/tickets.db")``
persists tickets to disk so they survive restarts.
"""
from __future__ import annotations

import json
import sqlite3
import threading
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional

STATUSES = ["Open", "In progress", "Resolved"]

_SCHEMA = """
CREATE TABLE IF NOT EXISTS tickets (
    ref                 TEXT PRIMARY KEY,
    created             TEXT NOT NULL,
    name                TEXT NOT NULL,
    email               TEXT NOT NULL,
    text                TEXT NOT NULL,
    category            TEXT NOT NULL,
    category_confidence REAL NOT NULL,
    priority            TEXT NOT NULL,
    sentiment           TEXT NOT NULL,
    sla                 TEXT NOT NULL,
    escalate            INTEGER NOT NULL,
    suggested_reply     TEXT NOT NULL,
    related             TEXT NOT NULL,
    status              TEXT NOT NULL DEFAULT 'Open'
)
"""


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


def _row_to_record(row: sqlite3.Row) -> TicketRecord:
    return TicketRecord(
        ref=row["ref"], created=datetime.fromisoformat(row["created"]), name=row["name"],
        email=row["email"], text=row["text"], category=row["category"],
        category_confidence=row["category_confidence"], priority=row["priority"],
        sentiment=row["sentiment"], sla=row["sla"], escalate=bool(row["escalate"]),
        suggested_reply=row["suggested_reply"], related=json.loads(row["related"]),
        status=row["status"],
    )


class TicketStore:
    def __init__(self, path: Optional[str] = None) -> None:
        self._lock = threading.Lock()
        if path:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
        self._db = sqlite3.connect(path or ":memory:", check_same_thread=False)
        self._db.row_factory = sqlite3.Row
        if path:
            self._db.execute("PRAGMA journal_mode=WAL")
        self._db.execute(_SCHEMA)
        self._db.commit()

    def add(self, text: str, result, name: str = "", email: str = "",
            related: Optional[List[str]] = None) -> TicketRecord:
        with self._lock:
            ref = self._new_ref()
            rec = TicketRecord(
                ref=ref, created=datetime.now(), name=name.strip(), email=email.strip(),
                text=text.strip(), category=result.category,
                category_confidence=result.category_confidence, priority=result.priority,
                sentiment=result.sentiment, sla=result.sla, escalate=result.escalate,
                suggested_reply=result.suggested_reply, related=list(related or []),
            )
            self._db.execute(
                "INSERT INTO tickets VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (rec.ref, rec.created.isoformat(), rec.name, rec.email, rec.text, rec.category,
                 rec.category_confidence, rec.priority, rec.sentiment, rec.sla, int(rec.escalate),
                 rec.suggested_reply, json.dumps(rec.related), rec.status))
            self._db.commit()
            return rec

    def _new_ref(self) -> str:
        while True:
            ref = "TIQ-" + uuid.uuid4().hex[:6].upper()
            if self._db.execute("SELECT 1 FROM tickets WHERE ref=?", (ref,)).fetchone() is None:
                return ref

    def get(self, ref: str) -> Optional[TicketRecord]:
        with self._lock:
            row = self._db.execute("SELECT * FROM tickets WHERE ref=?", (ref.strip().upper(),)).fetchone()
        return _row_to_record(row) if row else None

    def all(self) -> List[TicketRecord]:
        """All tickets, newest first."""
        with self._lock:
            rows = self._db.execute("SELECT * FROM tickets ORDER BY created DESC, rowid DESC").fetchall()
        return [_row_to_record(r) for r in rows]

    def set_status(self, ref: str, status: str) -> bool:
        if status not in STATUSES:
            raise ValueError(f"Unknown status: {status}")
        with self._lock:
            cur = self._db.execute("UPDATE tickets SET status=? WHERE ref=?", (status, ref.strip().upper()))
            self._db.commit()
            return cur.rowcount > 0

    def clear(self) -> None:
        with self._lock:
            self._db.execute("DELETE FROM tickets")
            self._db.commit()

    def close(self) -> None:
        with self._lock:
            self._db.close()
