"""Styling and small HTML helpers for the Streamlit UI."""
from __future__ import annotations

import html
from typing import Iterable

import streamlit as st

CSS = """
<style>
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stMainMenu"],
[data-testid="stDeployButton"], [data-testid="stDecoration"] { display: none !important; }
header[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 2rem; max-width: 1100px; }

.hero {
  border-radius: 20px; padding: 2.2rem 2.4rem; margin-bottom: 1.4rem; color: #fff;
  background: radial-gradient(1200px 400px at 90% -20%, rgba(34,211,238,.45), transparent),
              linear-gradient(135deg, #4f46e5 0%, #7c3aed 55%, #db2777 100%);
  box-shadow: 0 12px 40px rgba(79,70,229,.35);
}
.hero h1 { margin: 0 0 .3rem 0; font-size: 2.3rem; font-weight: 800; letter-spacing: -.02em; color:#fff; }
.hero p { margin: 0; font-size: 1.05rem; opacity: .92; }
.pills { margin-top: 1rem; display: flex; gap: .5rem; flex-wrap: wrap; }
.pill { background: rgba(255,255,255,.18); border: 1px solid rgba(255,255,255,.3);
        padding: .25rem .75rem; border-radius: 999px; font-size: .82rem; backdrop-filter: blur(6px); }

.card { border: 1px solid rgba(128,128,160,.28); border-radius: 16px; padding: 1rem 1.2rem;
        background: rgba(128,128,160,.07); height: 100%; }
.card .label { font-size: .75rem; text-transform: uppercase; letter-spacing: .08em; opacity: .65; }
.card .value { font-size: 1.45rem; font-weight: 700; margin-top: .2rem; }
.card .sub { font-size: .82rem; opacity: .65; margin-top: .15rem; }

.badge { display: inline-block; padding: .18rem .65rem; border-radius: 999px; font-size: .8rem;
         font-weight: 600; border: 1px solid transparent; }
.b-high, .b-negative { background: rgba(239,68,68,.15); color: #f87171; border-color: rgba(239,68,68,.4); }
.b-medium { background: rgba(245,158,11,.15); color: #fbbf24; border-color: rgba(245,158,11,.4); }
.b-low, .b-positive { background: rgba(34,197,94,.15); color: #4ade80; border-color: rgba(34,197,94,.4); }
.b-neutral { background: rgba(148,163,184,.15); color: #94a3b8; border-color: rgba(148,163,184,.4); }
.b-cat { background: rgba(99,102,241,.15); color: #a5b4fc; border-color: rgba(99,102,241,.4); }

.timeline { display: flex; align-items: center; margin: 1rem 0 .4rem 0; }
.step { display: flex; flex-direction: column; align-items: center; flex: 0 0 auto; min-width: 90px;
        font-size: .8rem; opacity: .5; }
.step .dot { width: 26px; height: 26px; border-radius: 50%; display: grid; place-items: center;
             background: rgba(128,128,160,.3); font-size: .8rem; margin-bottom: .3rem; }
.step.done { opacity: 1; }
.step.done .dot { background: linear-gradient(135deg,#4f46e5,#7c3aed); color: #fff; }
.step.current { opacity: 1; font-weight: 700; }
.step.current .dot { box-shadow: 0 0 0 4px rgba(124,58,237,.3); }
.bar { flex: 1; height: 3px; background: rgba(128,128,160,.3); margin-bottom: 1.2rem; }
.bar.done { background: linear-gradient(90deg,#4f46e5,#7c3aed); }

.bubble-row { display: flex; gap: .75rem; align-items: flex-start; margin: .6rem 0; }
.avatar { width: 38px; height: 38px; border-radius: 50%; flex: 0 0 38px; display: grid; place-items: center;
          background: linear-gradient(135deg,#4f46e5,#db2777); color: #fff; font-size: 1.1rem; }
.bubble { border: 1px solid rgba(128,128,160,.28); background: rgba(99,102,241,.08);
          border-radius: 4px 16px 16px 16px; padding: .8rem 1rem; line-height: 1.5; }
.bubble .who { font-size: .72rem; opacity: .6; margin-bottom: .2rem; text-transform: uppercase; letter-spacing: .08em; }

.chip { display: inline-block; margin: .2rem .35rem .2rem 0; padding: .3rem .8rem; border-radius: 999px;
        border: 1px solid rgba(128,128,160,.35); font-size: .85rem; background: rgba(128,128,160,.08); }
.escalate { border: 1px solid rgba(239,68,68,.5); background: rgba(239,68,68,.12); color: #fca5a5;
            border-radius: 14px; padding: .8rem 1.1rem; font-weight: 600; margin-bottom: 1rem; }
.stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primaryFormSubmit"] {
  background: linear-gradient(135deg,#4f46e5,#7c3aed); border: 0; font-weight: 600; }
.small { font-size: .8rem; opacity: .6; }
</style>
"""

STEPS = ["Received", "Triaged", "In progress", "Resolved"]
STATUS_STEP = {"Open": 1, "In progress": 2, "Resolved": 3}


def inject() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def _e(x: object) -> str:
    return html.escape(str(x))


def hero(title: str, subtitle: str, pills: Iterable[str] = ()) -> None:
    ps = "".join(f'<span class="pill">{_e(p)}</span>' for p in pills)
    st.markdown(f'<div class="hero"><h1>{_e(title)}</h1><p>{_e(subtitle)}</p>'
                f'<div class="pills">{ps}</div></div>', unsafe_allow_html=True)


def badge(text: str, kind: str) -> str:
    return f'<span class="badge b-{_e(kind)}">{_e(text)}</span>'


def card(label: str, value: str, sub: str = "", raw_value: bool = False) -> None:
    v = value if raw_value else _e(value)
    s = f'<div class="sub">{_e(sub)}</div>' if sub else ""
    st.markdown(f'<div class="card"><div class="label">{_e(label)}</div>'
                f'<div class="value">{v}</div>{s}</div>', unsafe_allow_html=True)


def timeline(status: str) -> None:
    cur = STATUS_STEP.get(status, 1)
    parts = []
    for i, name in enumerate(STEPS):
        cls = "done" if i < cur or (i == cur and status == "Resolved") else ("current" if i == cur else "")
        mark = "✓" if cls == "done" else str(i + 1)
        parts.append(f'<div class="step {cls}"><div class="dot">{mark}</div>{_e(name)}</div>')
        if i < len(STEPS) - 1:
            parts.append(f'<div class="bar {"done" if i < cur else ""}"></div>')
    st.markdown(f'<div class="timeline">{"".join(parts)}</div>', unsafe_allow_html=True)


def bubble(text: str, who: str = "TicketIQ Assistant") -> None:
    st.markdown(f'<div class="bubble-row"><div class="avatar">✦</div><div class="bubble">'
                f'<div class="who">{_e(who)}</div>{_e(text)}</div></div>', unsafe_allow_html=True)


def chips(items: Iterable[str]) -> None:
    st.markdown("".join(f'<span class="chip">{_e(i)}</span>' for i in items), unsafe_allow_html=True)


def escalation_banner(msg: str) -> None:
    st.markdown(f'<div class="escalate">🚨 {_e(msg)}</div>', unsafe_allow_html=True)
