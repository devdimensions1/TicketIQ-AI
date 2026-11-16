"""Streamlit demo UI: streamlit run app.py"""
from __future__ import annotations

import uuid

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


TEAM = {
    "billing": "Billing",
    "technical": "Technical Support",
    "account": "Account",
    "feature_request": "Product",
}


def customer_portal(engine: TriageEngine) -> None:
    st.title("How can we help?")
    st.write("Tell us what's going on and we'll route your request to the right team.")
    with st.form("support_form", clear_on_submit=False):
        name = st.text_input("Your name (optional)")
        email = st.text_input("Email (optional)", placeholder="you@company.com")
        text = st.text_area("Describe your issue", height=160,
                            placeholder="What happened? What did you expect?")
        submitted = st.form_submit_button("Submit request", type="primary")
    if not submitted:
        return
    try:
        r = engine.triage(text, k=3)
    except ValueError:
        st.warning("Please describe your issue so we can help.")
        return
    ref = "TIQ-" + uuid.uuid4().hex[:6].upper()
    greet = f"Thanks, {name.strip()}!" if name.strip() else "Thanks for reaching out!"
    st.success(f"{greet} Your request **{ref}** has been received.")
    c1, c2 = st.columns(2)
    c1.metric("Handled by", TEAM.get(r.category, "Support"))
    c2.metric("Expected response", r.sla)
    if email.strip():
        st.caption(f"We'll send updates to {email.strip()}.")
    st.subheader("While you wait")
    st.info(r.suggested_reply)
    titles = []
    for t in r.similar_tickets:
        title = t["text"].split(". ")[0].strip(". ").capitalize()
        if title and title not in titles:
            titles.append(title)
    if titles:
        st.subheader("Related topics")
        for title in titles:
            st.markdown(f"- {title}")


def agent_console(engine: TriageEngine) -> None:
    st.title("🎫 TicketIQ AI: Agent Console")
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


def main() -> None:
    engine = get_engine()
    with st.sidebar:
        view = st.radio("View", ["Customer portal", "Agent console (internal)"])
        st.divider()
    if view == "Customer portal":
        customer_portal(engine)
    else:
        agent_console(engine)


main()
