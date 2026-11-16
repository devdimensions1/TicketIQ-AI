import pytest

from ticketiq.dataset import generate
from ticketiq.engine import TriageEngine
from ticketiq.replies import suggest_reply


@pytest.fixture(scope="module")
def engine():
    return TriageEngine()


def test_dataset_is_deterministic():
    assert generate(50, seed=1) == generate(50, seed=1)


def test_billing_ticket_classified(engine):
    r = engine.triage("I was charged twice and need a refund")
    assert r.category == "billing"


def test_urgent_angry_ticket_escalates(engine):
    r = engine.triage("Production is down for all our users. This is unacceptable. Need help immediately.")
    assert r.escalate and r.priority == "high"


def test_similar_tickets_returned(engine):
    r = engine.triage("The app crashes when I open the dashboard", k=3)
    assert len(r.similar_tickets) == 3


def test_empty_text_rejected(engine):
    with pytest.raises(ValueError):
        engine.triage("   ")


def test_reply_mentions_sla():
    assert "within 1 hour" in suggest_reply("billing", "high", "negative")
