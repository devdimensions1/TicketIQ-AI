from __future__ import annotations

import pytest

from ticketiq.engine import TriageEngine
from ticketiq.store import TicketStore


@pytest.fixture(scope="module")
def engine():
    return TriageEngine()


def test_add_get_and_status(engine):
    store = TicketStore()
    text = "I was charged twice and need a refund"
    rec = store.add(text, engine.triage(text), name=" Sam ", email="s@x.com")
    assert rec.ref.startswith("TIQ-") and rec.name == "Sam" and rec.status == "Open"
    assert store.get(rec.ref.lower()).ref == rec.ref
    assert store.set_status(rec.ref, "Resolved") and store.get(rec.ref).status == "Resolved"
    assert store.get("TIQ-NOPE") is None
    assert store.set_status("TIQ-NOPE", "Open") is False
    with pytest.raises(ValueError):
        store.set_status(rec.ref, "Bogus")


def test_all_newest_first_and_clear(engine):
    store = TicketStore()
    a = store.add("app crashes", engine.triage("app crashes"))
    b = store.add("dark mode please", engine.triage("dark mode please"))
    assert [r.ref for r in store.all()] == [b.ref, a.ref]
    store.clear()
    assert store.all() == []
