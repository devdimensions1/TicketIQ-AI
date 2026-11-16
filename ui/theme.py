"""Styling and small HTML helpers for the Streamlit UI."""
from __future__ import annotations

import html
from typing import Iterable

import streamlit as st

CSS = """
<style>
#MainMenu, footer, [data-testid="stToolbarActions"], [data-testid="stMainMenu"],
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

.card { border: 1px solid var(--bd); border-radius: 16px; padding: 1rem 1.2rem;
        background: var(--card); height: 100%; }
.card .label { font-size: .75rem; text-transform: uppercase; letter-spacing: .08em; opacity: .65; }
.card .value { font-size: 1.45rem; font-weight: 700; margin-top: .2rem; }
.card .sub { font-size: .82rem; opacity: .65; margin-top: .15rem; }

.badge { display: inline-block; padding: .18rem .65rem; border-radius: 999px; font-size: .8rem;
         font-weight: 600; border: 1px solid transparent; }
.stApp .b-high, .stApp .b-negative { background: rgba(239,68,68,.15); color: var(--c-red) !important; border-color: rgba(239,68,68,.4); }
.stApp .b-medium { background: rgba(245,158,11,.15); color: var(--c-amb) !important; border-color: rgba(245,158,11,.4); }
.stApp .b-low, .stApp .b-positive { background: rgba(34,197,94,.15); color: var(--c-grn) !important; border-color: rgba(34,197,94,.4); }
.stApp .b-neutral { background: rgba(148,163,184,.15); color: var(--c-gry) !important; border-color: rgba(148,163,184,.4); }
.stApp .b-cat { background: rgba(99,102,241,.15); color: var(--c-ind) !important; border-color: rgba(99,102,241,.4); }

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
.bubble { border: 1px solid var(--bd); background: rgba(99,102,241,.08);
          border-radius: 4px 16px 16px 16px; padding: .8rem 1rem; line-height: 1.5; }
.bubble .who { font-size: .72rem; opacity: .6; margin-bottom: .2rem; text-transform: uppercase; letter-spacing: .08em; }

.chip { display: inline-block; margin: .2rem .35rem .2rem 0; padding: .3rem .8rem; border-radius: 999px;
        border: 1px solid var(--bd); font-size: .85rem; background: var(--card); }
.escalate { border: 1px solid rgba(239,68,68,.5); background: rgba(239,68,68,.12); color: #fca5a5;
            border-radius: 14px; padding: .8rem 1.1rem; font-weight: 600; margin-bottom: 1rem; }
.stApp .escalate { color: var(--c-red) !important; }
.tblwrap { overflow: auto; max-height: 440px; border: 1px solid var(--bd); border-radius: 14px; margin: .4rem 0 1rem 0; }
.tbl { width: 100%; border-collapse: collapse; font-size: .85rem; }
.tbl th { position: sticky; top: 0; text-align: left; padding: .55rem .8rem; background: var(--bg2);
          font-size: .72rem; text-transform: uppercase; letter-spacing: .08em; opacity: .85; }
.tbl td { padding: .5rem .8rem; border-top: 1px solid var(--bd); vertical-align: middle; }
.tbl tr:hover td { background: var(--card); }
.meter { display: inline-block; width: 70px; height: 7px; border-radius: 99px; background: var(--bd);
         vertical-align: middle; margin-right: .5rem; overflow: hidden; }
.meter i { display: block; height: 100%; background: linear-gradient(90deg,#4f46e5,#db2777); }
.hbar { display: flex; align-items: center; gap: .7rem; margin: .45rem 0; font-size: .85rem; }
.hbar .nm { width: 120px; flex: 0 0 120px; }
.hbar .tr { flex: 1; height: 12px; border-radius: 99px; background: var(--bd); overflow: hidden; }
.hbar .tr i { display: block; height: 100%; border-radius: 99px; background: linear-gradient(90deg,#4f46e5,#7c3aed,#db2777); }
.hbar .ct { width: 28px; text-align: right; font-weight: 700; }
pre.code { border: 1px solid var(--bd); background: var(--card); border-radius: 12px; padding: .9rem 1rem;
           overflow: auto; font-size: .8rem; line-height: 1.45; }
.stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primaryFormSubmit"] {
  background: linear-gradient(135deg,#4f46e5,#7c3aed); border: 0; font-weight: 600; }
.small { font-size: .8rem; opacity: .6; }
.st-key-theme_btn { display: flex; justify-content: flex-end; }
.st-key-theme_btn button { border-radius: 999px !important; width: 2.6rem; height: 2.6rem; min-height: 0;
  padding: 0 !important; font-size: 1.15rem; }
</style>
"""

DARK_VARS = """
:root { --bg:#0e1117; --bg2:#161a23; --tx:#fafafa; --mut:rgba(250,250,250,.62); --inp:#262730;
  --card:rgba(128,128,160,.09); --bd:rgba(128,128,160,.30);
  --c-red:#f87171; --c-amb:#fbbf24; --c-grn:#4ade80; --c-gry:#94a3b8; --c-ind:#a5b4fc; }
"""
LIGHT_VARS = """
:root { --bg:#f5f6fb; --bg2:#ffffff; --tx:#1b1f2a; --mut:rgba(27,31,42,.62); --inp:#ffffff;
  --card:#ffffff; --bd:rgba(80,85,120,.22);
  --c-red:#b91c1c; --c-amb:#b45309; --c-grn:#15803d; --c-gry:#475569; --c-ind:#4338ca; }
"""
MODE_CSS = """
.stApp { background: var(--bg) !important; color: var(--tx); }
[data-testid="stSidebar"], [data-testid="stSidebar"] > div { background: var(--bg2) !important; }
.stApp :is(h1,h2,h3,h4,h5,h6,p,label,li,span,small,summary,th,td,div[data-testid="stMarkdownContainer"]) { color: var(--tx); }
.stApp [data-testid="stCaptionContainer"], .stApp [data-testid="stCaptionContainer"] * { color: var(--mut) !important; }
.stApp .hero, .stApp .hero * { color: #fff !important; }
.stApp .bubble .who, .stApp .card .label, .stApp .card .sub { color: var(--mut) !important; }
.stApp button[kind="primary"] *, .stApp button[kind="primaryFormSubmit"] * { color: #fff !important; }
.stApp button[kind="secondary"], .stApp button[kind="secondaryFormSubmit"] {
  background: var(--card) !important; border: 1px solid var(--bd) !important; }
.stApp button[kind="secondary"] *, .stApp button[kind="secondaryFormSubmit"] * { color: var(--tx) !important; }
.stApp [data-baseweb="input"], .stApp [data-baseweb="input"] > div, .stApp [data-baseweb="textarea"],
.stApp [data-baseweb="textarea"] > div, .stApp [data-baseweb="select"] > div {
  background: var(--inp) !important; border-color: var(--bd) !important; }
.stApp input, .stApp textarea { color: var(--tx) !important; -webkit-text-fill-color: var(--tx) !important; }
.stApp input::placeholder, .stApp textarea::placeholder { color: var(--mut) !important; -webkit-text-fill-color: var(--mut) !important; }
[data-baseweb="popover"] [data-baseweb="menu"], [data-baseweb="popover"] ul { background: var(--bg2) !important; }
[data-baseweb="popover"] li, [data-baseweb="popover"] li * { color: var(--tx) !important; }
.stApp [data-testid="stForm"], .stApp [data-testid="stExpander"] details, .stApp [data-testid="stStatus"] {
  border-color: var(--bd) !important; background: transparent !important; }
.stApp [data-testid="stFileUploaderDropzone"] { background: var(--inp) !important; border-color: var(--bd) !important; }
.stApp [data-baseweb="tab-border"] { background: var(--bd) !important; }
"""

STEPS = ["Received", "Triaged", "In progress", "Resolved"]
STATUS_STEP = {"Open": 1, "In progress": 2, "Resolved": 3}


def inject(dark: bool = True) -> None:
    vars_css = DARK_VARS if dark else LIGHT_VARS
    st.markdown(f"<style>{vars_css}{MODE_CSS}</style>" + CSS, unsafe_allow_html=True)


class Safe(str):
    """Marks a string as trusted HTML so tables don't escape it."""


def _cell(v: object) -> str:
    return str(v) if isinstance(v, Safe) else _e(v)


def table(rows: list, columns: Iterable[str] = ()) -> None:
    cols = list(columns) or (list(rows[0].keys()) if rows else [])
    head = "".join(f"<th>{_e(c)}</th>" for c in cols)
    body = "".join("<tr>" + "".join(f"<td>{_cell(r.get(c, ''))}</td>" for c in cols) + "</tr>" for r in rows)
    st.markdown(f'<div class="tblwrap"><table class="tbl"><thead><tr>{head}</tr></thead>'
                f'<tbody>{body}</tbody></table></div>', unsafe_allow_html=True)


def meter(value: float) -> Safe:
    pct = int(min(max(value, 0.0), 1.0) * 100)
    return Safe(f'<span class="meter"><i style="width:{pct}%"></i></span>{value:.2f}')


def bars(data: dict) -> None:
    top = max(data.values()) if data else 0
    rows = "".join(
        f'<div class="hbar"><span class="nm">{_e(k)}</span><span class="tr">'
        f'<i style="width:{(v / top * 100) if top else 0:.0f}%"></i></span><span class="ct">{v}</span></div>'
        for k, v in data.items())
    st.markdown(rows, unsafe_allow_html=True)


def code(text: str) -> None:
    st.markdown(f'<pre class="code">{_e(text)}</pre>', unsafe_allow_html=True)


def _e(x: object) -> str:
    return html.escape(str(x))


def hero(title: str, subtitle: str, pills: Iterable[str] = ()) -> None:
    ps = "".join(f'<span class="pill">{_e(p)}</span>' for p in pills)
    st.markdown(f'<div class="hero"><h1>{_e(title)}</h1><p>{_e(subtitle)}</p>'
                f'<div class="pills">{ps}</div></div>', unsafe_allow_html=True)


def badge(text: str, kind: str) -> Safe:
    return Safe(f'<span class="badge b-{_e(kind)}">{_e(text)}</span>')


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
