"""Streamlit demo UI: streamlit run app.py"""
from __future__ import annotations

import pandas as pd
import streamlit as st

from ticketiq.engine import TriageEngine

SAMPLES = {
    "Angry billing issue": "I was charged twice this month and I'm furious. Need a refund immediately!",
    "Production outage": "The app crashes every time I open the dashboard. Production is down for all our users.",
    "Feature request": "Would be great to have a dark mode. Thanks, love the product!",
    "Account how-to": "How do I add a new team member to our workspace? No rush.",
}
PRIORITY_ICON = {"high": "🔴", "medium": "🟠", "low": "🟢"}
SENTIMENT_ICON = {"negative": "😠", "neutral": "😐", "positive": "😊"}

st.set_page_config(page_title="TicketIQ AI", page_icon="🎫", layout="wide")


@st.cache_resource(show_spinner="Loading models (first run trains them)...")
def get_engine() -> TriageEngine:
    return TriageEngine()


def show_result(r) -> None:
    if r.escalate:
        st.error("🚨 ESCALATE: high priority with negative sentiment. Route to a senior agent.")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Category", r.category.replace("_", " ").title())
    c2.metric("Priority", f"{PRIORITY_ICON[r.priority]} {r.priority.title()}")
    c3.metric("Sentiment", f"{SENTIMENT_ICON[r.sentiment]} {r.sentiment.title()}")
    c4.metric("SLA", r.sla)
    st.caption("Category confidence")
    st.progress(min(max(r.category_confidence, 0.0), 1.0), text=f"{r.category_confidence:.0%}")

    st.subheader("Suggested reply")
    st.info(r.suggested_reply)

    st.subheader("Similar past tickets")
    if r.similar_tickets:
        st.dataframe(pd.DataFrame(r.similar_tickets), width="stretch", hide_index=True)
    else:
        st.write("No similar tickets found.")
    with st.expander("Raw JSON"):
        st.json(r.to_dict())


def main() -> None:
    engine = get_engine()
    st.title("🎫 TicketIQ AI")
    st.write("Paste a support ticket to get category, priority, SLA, sentiment, "
             "escalation and a suggested reply.")

    with st.sidebar:
        st.header("Settings")
        k = st.slider("Similar tickets to show", 1, 10, 3)
        st.header("Samples")
        for label, text in SAMPLES.items():
            if st.button(label, width="stretch"):
                st.session_state["ticket"] = text
        st.caption("Models are trained on synthetic data for demo purposes. "
                   "Accuracy figures are not real-world numbers.")

    tab_single, tab_batch = st.tabs(["Single ticket", "Batch (CSV)"])

    with tab_single:
        text = st.text_area("Ticket text", key="ticket", height=150,
                            placeholder="Describe the customer's issue...")
        if st.button("Triage", type="primary"):
            try:
                show_result(engine.triage(text, k=k))
            except ValueError as exc:
                st.warning(str(exc))

    with tab_batch:
        st.write("Upload a CSV with a `text` column.")
        up = st.file_uploader("CSV file", type="csv")
        if up is not None:
            df = pd.read_csv(up)
            if "text" not in df.columns:
                st.error("CSV must contain a `text` column.")
            else:
                rows = []
                for t in df["text"].fillna("").astype(str):
                    if not t.strip():
                        continue
                    r = engine.triage(t, k=1)
                    rows.append({"text": t, "category": r.category, "priority": r.priority,
                                 "sentiment": r.sentiment, "sla": r.sla, "escalate": r.escalate})
                out = pd.DataFrame(rows)
                st.dataframe(out, width="stretch", hide_index=True)
                st.download_button("Download results", out.to_csv(index=False),
                                   "triage_results.csv", "text/csv")


main()
