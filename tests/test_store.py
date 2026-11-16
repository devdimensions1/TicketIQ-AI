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


def test_persists_across_instances(engine, tmp_path):
    path = str(tmp_path / "sub" / "t.db")
    first = TicketStore(path)
    text = "Please delete my account and personal data"
    rec = first.add(text, engine.triage(text), name="Ana", email="a@x.com", related=["Delete account"])
    first.set_status(rec.ref, "In progress")
    first.close()

    second = TicketStore(path)
    got = second.get(rec.ref)
    assert got is not None and got.status == "In progress"
    assert got.name == "Ana" and got.related == ["Delete account"]
    assert got.created == rec.created and isinstance(got.escalate, bool)
    assert [r.ref for r in second.all()] == [rec.ref]
    second.clear()
    assert second.all() == []
    second.close()


def test_store_is_thread_safe(engine, tmp_path):
    import threading
    store = TicketStore(str(tmp_path / "t.db"))
    result = engine.triage("app crashes on login")

    def worker():
        for _ in range(10):
            store.add("app crashes on login", result)

    threads = [threading.Thread(target=worker) for _ in range(5)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    refs = {r.ref for r in store.all()}
    assert len(refs) == 50
    store.close()
