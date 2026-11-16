from fastapi.testclient import TestClient

from ticketiq.api import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json()["status"] == "ok"


def test_triage_endpoint():
    res = client.post("/triage", json={"text": "I cannot log in, error 500 on export"})
    assert res.status_code == 200
    assert res.json()["category"] == "technical"


def test_triage_validation():
    assert client.post("/triage", json={"text": ""}).status_code == 422


def test_batch():
    res = client.post("/triage/batch", json=[{"text": "dark mode please"}, {"text": "refund my payment"}])
    assert len(res.json()) == 2
