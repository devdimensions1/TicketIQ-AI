"""FastAPI service exposing the triage engine."""
from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from . import __version__
from .engine import TriageEngine

app = FastAPI(title="TicketIQ-AI", version=__version__,
              description="AI-powered support ticket triage")
_engine: TriageEngine | None = None


def get_engine() -> TriageEngine:
    global _engine
    if _engine is None:
        _engine = TriageEngine()
    return _engine


class TicketIn(BaseModel):
    text: str = Field(..., min_length=3, examples=["I was charged twice, please refund. This is urgent!"])


@app.get("/health")
def health():
    return {"status": "ok", "version": __version__}


@app.post("/triage")
def triage(ticket: TicketIn):
    try:
        return get_engine().triage(ticket.text).to_dict()
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))


@app.post("/triage/batch")
def triage_batch(tickets: list[TicketIn]):
    engine = get_engine()
    return [engine.triage(t.text).to_dict() for t in tickets]
