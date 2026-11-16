"""Streamlit demo UI: streamlit run app.py

Customer portal:  http://localhost:8501
Agent console:    http://localhost:8501/?view=agent
"""
from __future__ import annotations

import pandas as pd
import streamlit as st

from ticketiq.engine import TriageEngine
from ticketiq.store import STATUSES, TicketStore
from ui import theme

SAMPLES = {
    "💳 Double charged": "I was charged twice this month and I'm furious. Need a refund immediately!",
    "🔥 Production outage": "The app crashes every time I open the dashboard. Production is down for all our users.",
    "💡 Feature idea": "Would be great to have a dark mode. Thanks, love the product!",
    "👥 Add team member": "How do I add a new team member to our workspace? No rush.",
}
DEMO_TICKETS = list(SAMPLES.values()) + [
    "I cannot log in, it keeps saying my password is invalid. This is urgent!",
    "Please delete my account and all associated personal data.",
    "Can you add an option to export data directly to Excel?",
    "My invoice for last month never arrived, can you resend it?",
    "The system is extremely slow and pages take a minute to load. Terrible experience.",
]
TEAM = {"billing": "Billing", "technical": "Technical Support",
        "account": "Account", "feature_request": "Product"}
CATEGORY_ICON = {"billing": "💳", "technical": "🛠️", "account": "👤", "feature_request": "💡"}
PRIORITY_RANK = {"high": 0, "medium": 1, "low": 2}

st.set_page_config(page_title="TicketIQ AI", page_icon="🎫", layout="wide",
                   initial_sidebar_state="collapsed")


@st.cache_resource(show_spinner="Loading models (first run trains them)...")
def get_engine() -> TriageEngine:
    return TriageEngine()


@st.cache_resource
def get_store() -> TicketStore:
    # Shared by every browser session in this server process.
    return TicketStore()


def related_titles(similar: list) -> list:
    titles: list = []
    for t in similar:
        title = t["text"].split(". ")[0].strip(". ").capitalize()
        if title and title not in titles:
            titles.append(title)
    return titles


def submit_ticket(engine: TriageEngine, store: TicketStore, text: str,
                  name: str = "", email: str = ""):
    r = engine.triage(text, k=3)
    return store.add(text, r, name=name, email=email, related=related_titles(r.similar_tickets)), r


# ---------------------------------------------------------------- customer

def show_receipt(rec) -> None:
    greet = f"Thanks, {rec.name}!" if rec.name else "Thanks for reaching out!"
    st.success(f"{greet} Your request **{rec.ref}** has been received. Save this reference to track it.")
    c1, c2, c3 = st.columns(3)
    with c1:
        theme.card("Handled by", f"{CATEGORY_ICON.get(rec.category, '🎫')} {TEAM.get(rec.category, 'Support')}")
    with c2:
        theme.card("Expected response", rec.sla)
    with c3:
        theme.card("Status", rec.status)
    theme.timeline(rec.status)
    if rec.email:
        st.caption(f"We'll send updates to {rec.email}.")
    st.markdown("#### While you wait")
    theme.bubble(rec.suggested_reply)
    if rec.related:
        st.markdown("#### People with similar questions also asked about")
        theme.chips(rec.related)


def customer_portal(engine: TriageEngine, store: TicketStore) -> None:
    theme.hero("How can we help?",
               "Tell us what's going on and our AI will route your request to the right team instantly.",
               ["⚡ Instant routing", "🎯 Smart prioritisation", "🔒 Private & secure"])
    tab_new, tab_track = st.tabs(["✉️  New request", "🔎  Track a request"])

    with tab_new:
        st.caption("Not sure what to write? Try an example:")
        cols = st.columns(len(SAMPLES))
        for col, (label, text) in zip(cols, SAMPLES.items()):
            col.button(label, key=f"ex_{label}", width="stretch",
                       on_click=lambda t=text: st.session_state.update(cust_text=t))
        with st.form("support_form"):
            c1, c2 = st.columns(2)
            name = c1.text_input("Your name (optional)")
            email = c2.text_input("Email (optional)", placeholder="you@company.com")
            text = st.text_area("Describe your issue", key="cust_text", height=150,
                                placeholder="What happened? What did you expect?")
            submitted = st.form_submit_button("Submit request ➜", type="primary")
        if submitted:
            if not text.strip():
                st.warning("Please describe your issue so we can help.")
            else:
                with st.status("Analysing your request...", expanded=True) as status:
                    rec, r = submit_ticket(engine, store, text, name, email)
                    st.write(f"✓ Understood topic: **{r.category.replace('_', ' ')}**")
                    st.write(f"✓ Assessed urgency, response target **{r.sla}**")
                    st.write(f"✓ Routed to **{TEAM.get(r.category, 'Support')}**")
                    status.update(label="Request received", state="complete", expanded=False)
                st.session_state["last_ref"] = rec.ref
                show_receipt(rec)

    with tab_track:
        ref = st.text_input("Reference number", value=st.session_state.get("last_ref", ""),
                            placeholder="TIQ-XXXXXX")
        if ref.strip():
            rec = store.get(ref)
            if rec is None:
                st.warning("We couldn't find that reference. Check it and try again.")
            else:
                show_receipt(rec)
        st.caption("Demo note: requests are held in memory and cleared when the app restarts.")


# ------------------------------------------------------------------- agent

def show_result(r) -> None:
    if r.escalate:
        theme.escalation_banner("ESCALATE: high priority with negative sentiment. Route to a senior agent.")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        theme.card("Category", f"{CATEGORY_ICON.get(r.category, '')} {r.category.replace('_', ' ').title()}")
    with c2:
        theme.card("Priority", theme.badge(r.priority.title(), r.priority), raw_value=True)
    with c3:
        theme.card("Sentiment", theme.badge(r.sentiment.title(), r.sentiment), raw_value=True)
    with c4:
        theme.card("SLA", r.sla)
    st.caption("Category confidence")
    st.progress(min(max(r.category_confidence, 0.0), 1.0), text=f"{r.category_confidence:.0%}")
    st.markdown("#### Suggested reply")
    theme.bubble(r.suggested_reply, who="Draft reply")
    st.markdown("#### Similar past tickets")
    if r.similar_tickets:
        st.dataframe(pd.DataFrame(r.similar_tickets), width="stretch", hide_index=True,
                     column_config={"similarity": st.column_config.ProgressColumn(
                         "similarity", min_value=0.0, max_value=1.0, format="%.2f")})
    else:
        st.write("No similar tickets found.")
    with st.expander("Raw JSON"):
        st.json(r.to_dict())


def queue_frame(records: list) -> pd.DataFrame:
    rows = sorted(records, key=lambda r: (not r.escalate, PRIORITY_RANK[r.priority],
                                          -r.created.timestamp()))
    return pd.DataFrame([{
        "ref": r.ref, "🚨": "🚨" if r.escalate else "", "priority": r.priority,
        "category": r.category, "sentiment": r.sentiment, "sla": r.sla,
        "status": r.status, "created": r.created.strftime("%H:%M:%S"),
        "ticket": r.text,
    } for r in rows])


def agent_console(engine: TriageEngine, store: TicketStore) -> None:
    theme.hero("Agent Console", "Triage, prioritise and resolve tickets with AI assistance.",
               ["🧠 TF-IDF + Logistic Regression", "📴 Runs fully offline", "⚠️ Synthetic demo data"])
    with st.sidebar:
        st.header("Tools")
        k = st.slider("Similar tickets to show", 1, 10, 3)
        if st.button("Load demo tickets", width="stretch"):
            for t in DEMO_TICKETS:
                submit_ticket(engine, store, t)
            st.rerun()
        if st.button("Clear queue", width="stretch"):
            store.clear()
            st.rerun()
        st.header("Samples")
        for label, text in SAMPLES.items():
            if st.button(label, key=f"s_{label}", width="stretch"):
                st.session_state["ticket"] = text
        st.caption("Models are trained on synthetic data. Accuracy figures are not real-world numbers.")

    tab_queue, tab_triage, tab_batch = st.tabs(["📥 Queue & insights", "🧪 Triage a ticket", "📦 Batch (CSV)"])

    with tab_queue:
        records = store.all()
        if not records:
            st.info("The queue is empty. Submit a request from the customer portal, "
                    "or click **Load demo tickets** in the sidebar.")
        else:
            open_n = sum(r.status != "Resolved" for r in records)
            esc_n = sum(r.escalate and r.status != "Resolved" for r in records)
            avg_conf = sum(r.category_confidence for r in records) / len(records)
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                theme.card("Total tickets", str(len(records)))
            with m2:
                theme.card("Open", str(open_n))
            with m3:
                theme.card("Escalated", str(esc_n), "needs senior agent")
            with m4:
                theme.card("Avg confidence", f"{avg_conf:.0%}")
            st.write("")
            ch1, ch2 = st.columns(2)
            df = queue_frame(records)
            ch1.markdown("##### Tickets by category")
            ch1.bar_chart(df["category"].value_counts())
            ch2.markdown("##### Tickets by priority")
            ch2.bar_chart(df["priority"].value_counts().reindex(["high", "medium", "low"]).fillna(0))
            st.markdown("##### Queue (escalations first)")
            st.dataframe(df, width="stretch", hide_index=True)
            st.markdown("##### Update a ticket")
            u1, u2, u3 = st.columns([2, 2, 1])
            ref = u1.selectbox("Ticket", [r.ref for r in records])
            new_status = u2.selectbox("Status", STATUSES)
            u3.write("")
            u3.write("")
            if u3.button("Update", type="primary", width="stretch"):
                store.set_status(ref, new_status)
                st.rerun()

    with tab_triage:
        text = st.text_area("Ticket text", key="ticket", height=140,
                            placeholder="Paste a customer's message...")
        add = st.checkbox("Add to queue", value=True)
        if st.button("Triage", type="primary"):
            try:
                r = engine.triage(text, k=k)
                if add:
                    rec = store.add(text, r, related=related_titles(r.similar_tickets))
                    st.caption(f"Added to queue as {rec.ref}")
                show_result(r)
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
                b1, b2 = st.columns(2)
                b1.bar_chart(out["category"].value_counts())
                b2.bar_chart(out["priority"].value_counts())
                st.dataframe(out, width="stretch", hide_index=True)
                st.download_button("Download results", out.to_csv(index=False),
                                   "triage_results.csv", "text/csv")


def main() -> None:
    theme.inject()
    engine, store = get_engine(), get_store()
    # Internal console lives at /?view=agent. This hides it from customers
    # but is not access control; put real authentication in front for production.
    if st.query_params.get("view") == "agent":
        agent_console(engine, store)
    else:
        customer_portal(engine, store)


main()
