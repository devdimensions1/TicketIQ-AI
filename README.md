# TicketIQ-AI

AI-powered support ticket triage engine built with Python, scikit-learn and FastAPI.
Paste in a customer ticket and TicketIQ instantly returns:

- **Category** (billing, technical, account, feature request) with confidence
- **Priority** and **SLA** target
- **Sentiment** analysis
- **Auto-escalation** flag for urgent, negative tickets
- **Suggested reply**, tone-adjusted to the customer's sentiment
- **Similar past tickets** for faster resolution

Runs fully offline: no API keys, no customer data leaves the machine.

## Architecture

```
ticketiq/
  dataset.py   synthetic labelled ticket generator
  models.py    TF-IDF + Logistic Regression classifiers (category / priority / sentiment)
  search.py    cosine-similarity retrieval of similar tickets
  replies.py   sentiment-aware reply templates + SLA mapping
  engine.py    TriageEngine orchestrating all components
  api.py       FastAPI service (/triage, /triage/batch, /health)
demo.py        CLI demo
tests/         pytest suite
```

## Quick start

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python -m ticketiq.models      # generate data + train models (prints accuracy)
python demo.py                 # CLI demo
uvicorn ticketiq.api:app --reload   # API docs at http://127.0.0.1:8000/docs
streamlit run app.py           # customer portal at http://localhost:8501
                               # agent console at http://localhost:8501/?view=agent
pytest                         # run tests
```

## Ticket storage

Submitted tickets are saved to a local SQLite database (`data/tickets.db`, gitignored), so the
queue and ticket statuses survive restarts. Set `TICKETIQ_DB=/path/to/file.db` to use another
location. The file holds customer names and emails in plain text, so treat it as sensitive and
use a proper database with access controls for production.

## Example

```bash
curl -X POST http://127.0.0.1:8000/triage \
  -H "Content-Type: application/json" \
  -d '{"text": "I was charged twice and I am furious. Need a refund immediately!"}'
```

```json
{
  "category": "billing",
  "category_confidence": 0.96,
  "priority": "high",
  "sentiment": "negative",
  "sla": "within 1 hour",
  "escalate": true,
  "suggested_reply": "We're truly sorry for the trouble ...",
  "similar_tickets": [...]
}
```

## Roadmap

- Swap the TF-IDF models for transformer embeddings or an LLM backend
- Connect to Zendesk / Freshdesk / Intercom webhooks
- Feedback loop for continuous retraining

Built by DevDimensions.
