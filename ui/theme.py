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
.block-container { padding-top: 1.2rem; max-width: 1240px; }
html, body, .stApp { font-family: Inter, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif; }

.hero {
  position: relative; overflow: hidden; border-radius: 16px; padding: 2.4rem 2.6rem; margin-bottom: 1.4rem; color: #fff;
  background: radial-gradient(900px 320px at 95% -30%, rgba(34,211,238,.40), transparent),
              linear-gradient(120deg, #3730a3 0%, #5b21b6 55%, #9d174d 100%);
  box-shadow: 0 10px 30px rgba(55,48,163,.28);
}
.hero::after { content: ""; position: absolute; inset: 0; pointer-events: none; opacity: .18;
  background-image: radial-gradient(rgba(255,255,255,.9) 1px, transparent 1px); background-size: 22px 22px;
  mask-image: linear-gradient(90deg, transparent 35%, #000 100%); -webkit-mask-image: linear-gradient(90deg, transparent 35%, #000 100%); }
.hero .eyebrow { font-size: .72rem; letter-spacing: .16em; text-transform: uppercase; opacity: .8; margin-bottom: .5rem; font-weight: 600; }
.hero h1 { margin: 0 0 .4rem 0; font-size: 2.2rem; font-weight: 750; letter-spacing: -.025em; color:#fff; position: relative; }
.hero p { margin: 0; font-size: 1.02rem; opacity: .9; max-width: 640px; position: relative; }
.trust { margin-top: 1.3rem; display: flex; gap: 1.6rem; flex-wrap: wrap; font-size: .85rem; position: relative; }
.trust span { display: inline-flex; align-items: center; gap: .45rem; opacity: .95; }

.st-key-navbar { border-bottom: 1px solid var(--bd); padding-bottom: .9rem; margin-bottom: 1.3rem; }
.brand { display: flex; align-items: center; gap: .65rem; }
.brand .logo { width: 34px; height: 34px; border-radius: 9px; display: grid; place-items: center; color: #fff;
  background: linear-gradient(135deg,#4f46e5,#9333ea 60%,#db2777); box-shadow: 0 4px 12px rgba(99,70,229,.4); }
.brand .name { font-weight: 800; font-size: 1.15rem; letter-spacing: -.02em; }
.brand .sep { width: 1px; height: 20px; background: var(--bd); margin: 0 .2rem; }
.brand .sect { font-size: .9rem; opacity: .7; }
.brand .env { font-size: .68rem; font-weight: 700; letter-spacing: .08em; padding: .15rem .5rem; border-radius: 6px;
  border: 1px solid var(--bd); opacity: .75; text-transform: uppercase; }

.rail { border: 1px solid var(--bd); border-radius: 14px; padding: 1.1rem 1.2rem; background: var(--card); margin-bottom: 1rem; }
.rail h4 { margin: 0 0 .8rem 0; font-size: .72rem; text-transform: uppercase; letter-spacing: .12em; opacity: .65; font-weight: 700; }
.sla-row { display: flex; align-items: center; justify-content: space-between; padding: .5rem 0; border-top: 1px solid var(--bd); font-size: .88rem; }
.sla-row:first-of-type { border-top: 0; }
.sla-row .dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; margin-right: .55rem; }
.how { display: flex; gap: .8rem; padding: .45rem 0; font-size: .88rem; line-height: 1.4; }
.how .n { flex: 0 0 24px; height: 24px; border-radius: 50%; display: grid; place-items: center; font-size: .72rem; font-weight: 700;
  background: rgba(99,102,241,.15); color: var(--c-ind); }
.how b { display: block; }
.how span.d { opacity: .65; font-size: .82rem; }
.panel-title { font-size: .72rem; text-transform: uppercase; letter-spacing: .12em; opacity: .65; font-weight: 700; margin: .2rem 0 .6rem 0; }
.page-title { font-size: 1.5rem; font-weight: 750; letter-spacing: -.02em; margin: 0; }
.page-sub { opacity: .65; font-size: .92rem; margin: .15rem 0 1rem 0; }
.footer { margin-top: 3rem; padding-top: 1rem; border-top: 1px solid var(--bd); font-size: .78rem; opacity: .6;
  display: flex; justify-content: space-between; flex-wrap: wrap; gap: .5rem; }
.ic { display: inline-flex; vertical-align: middle; }
.cardhead { display: flex; justify-content: space-between; align-items: center; }
.cardhead .chip-ic { width: 30px; height: 30px; border-radius: 8px; display: grid; place-items: center;
  background: rgba(99,102,241,.14); color: var(--c-ind); }
.stApp div[data-testid="stVerticalBlockBorderWrapper"] { border-color: var(--bd) !important; border-radius: 14px !important; background: var(--card); }
.card { border: 1px solid var(--bd); border-radius: 14px; padding: 1rem 1.2rem;
        background: var(--card); height: 100%; min-height: 112px; }
.card .label { font-size: .72rem; text-transform: uppercase; letter-spacing: .1em; opacity: .65; font-weight: 600; }
.card .value { font-size: 1.45rem; font-weight: 700; margin-top: .2rem; }
.card .sub { font-size: .82rem; opacity: .65; margin-top: .15rem; }

.badge { display: inline-block; white-space: nowrap; padding: .18rem .65rem; border-radius: 999px; font-size: .8rem;
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
.tbl td:first-child { white-space: nowrap; font-variant-numeric: tabular-nums; }
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
.stApp .brand .logo, .stApp .brand .logo * { color: #fff !important; }
.stApp .bubble .who, .stApp .card .label, .stApp .card .sub { color: var(--mut) !important; }
.stApp button[kind="primary"] *, .stApp button[kind="primaryFormSubmit"] * { color: #fff !important; }
.stApp button[kind="secondary"], .stApp button[kind="secondaryFormSubmit"] {
  background: var(--card) !important; border: 1px solid var(--bd) !important; }
.stApp button[kind="secondary"] *, .stApp button[kind="secondaryFormSubmit"] * { color: var(--tx) !important; }
.stApp [data-baseweb="input"], .stApp [data-baseweb="input"] > div, .stApp [data-baseweb="textarea"],
.stApp [data-baseweb="textarea"] > div, .stApp [data-baseweb="select"] > div {
  background: var(--inp) !important; border-color: var(--bd) !important; }
.stApp [data-baseweb="select"] *, .stApp [data-baseweb="tag"] * { color: var(--tx) !important; }
.stApp [data-baseweb="select"] svg { fill: var(--mut) !important; }
.stApp input, .stApp textarea { caret-color: var(--tx) !important; color: var(--tx) !important; -webkit-text-fill-color: var(--tx) !important; }
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


def bars(data: dict, min_rows: int = 0) -> None:
    top = max(data.values()) if data else 0
    pad = '<div class="hbar" style="visibility:hidden"><span class="nm">-</span></div>' * max(0, min_rows - len(data))
    rows = "".join(
        f'<div class="hbar"><span class="nm">{_e(k)}</span><span class="tr">'
        f'<i style="width:{(v / top * 100) if top else 0:.0f}%"></i></span><span class="ct">{v}</span></div>'
        for k, v in data.items()) + pad
    st.markdown(rows, unsafe_allow_html=True)


def code(text: str) -> None:
    st.markdown(f'<pre class="code">{_e(text)}</pre>', unsafe_allow_html=True)


def _e(x: object) -> str:
    return html.escape(str(x))


ICONS = {
    "bolt": '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "users": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/>'
             '<path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "inbox": '<polyline points="22 12 16 12 14 15 10 15 8 12 2 12"/>'
             '<path d="M5.45 5.11L2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/>',
    "alert": '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>'
             '<line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
    "check": '<polyline points="20 6 9 17 4 12"/>',
    "layers": '<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>',
    "activity": '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
}


def icon(name: str, size: int = 16) -> Safe:
    return Safe(f'<span class="ic"><svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
                f'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
                f'stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg></span>')


def hero(title: str, subtitle: str, items: Iterable = (), eyebrow: str = "") -> None:
    its = "".join(f"<span>{icon(i, 15)}{_e(t)}</span>" for i, t in items)
    eb = f'<div class="eyebrow">{_e(eyebrow)}</div>' if eyebrow else ""
    st.markdown(f'<div class="hero">{eb}<h1>{_e(title)}</h1><p>{_e(subtitle)}</p>'
                f'<div class="trust">{its}</div></div>', unsafe_allow_html=True)


def brand(section: str, env: str = "") -> None:
    pill = f'<span class="env">{_e(env)}</span>' if env else ""
    st.markdown(f'<div class="brand"><span class="logo">{icon("layers", 18)}</span>'
                f'<span class="name">TicketIQ</span><span class="sep"></span>'
                f'<span class="sect">{_e(section)}</span>{pill}</div>', unsafe_allow_html=True)


def rail_sla(rows: list) -> None:
    colors = {"high": "#ef4444", "medium": "#f59e0b", "low": "#22c55e"}
    body = "".join(f'<div class="sla-row"><span><span class="dot" style="background:{colors[k]}"></span>'
                   f'{_e(k.title())} priority</span><b>{_e(v)}</b></div>' for k, v in rows)
    st.markdown(f'<div class="rail"><h4>Response targets</h4>{body}</div>', unsafe_allow_html=True)


def rail_steps(steps: list) -> None:
    body = "".join(f'<div class="how"><span class="n">{i}</span><div><b>{_e(t)}</b>'
                   f'<span class="d">{_e(d)}</span></div></div>' for i, (t, d) in enumerate(steps, 1))
    st.markdown(f'<div class="rail"><h4>How it works</h4>{body}</div>', unsafe_allow_html=True)


def page_header(title: str, sub: str) -> None:
    st.markdown(f'<p class="page-title">{_e(title)}</p><p class="page-sub">{_e(sub)}</p>', unsafe_allow_html=True)


def panel_title(text: str) -> None:
    st.markdown(f'<div class="panel-title">{_e(text)}</div>', unsafe_allow_html=True)


def footer(note: str) -> None:
    from datetime import datetime
    st.markdown(f'<div class="footer"><span>© {datetime.now().year} TicketIQ · Privacy · Terms · Security</span>'
                f'<span>{_e(note)}</span></div>', unsafe_allow_html=True)


def badge(text: str, kind: str) -> Safe:
    return Safe(f'<span class="badge b-{_e(kind)}">{_e(text)}</span>')


def card(label: str, value: str, sub: str = "", raw_value: bool = False, icon_name: str = "") -> None:
    v = value if raw_value else _e(value)
    s_ = f'<div class="sub">{_e(sub)}</div>' if sub else ""
    chip = f'<span class="chip-ic">{icon(icon_name, 16)}</span>' if icon_name else ""
    st.markdown(f'<div class="card"><div class="cardhead"><div class="label">{_e(label)}</div>{chip}</div>'
                f'<div class="value">{v}</div>{s_}</div>', unsafe_allow_html=True)


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


def bubble(text: str, who: str = "TicketIQ Assistant", avatar: str = "✦") -> None:
    st.markdown(f'<div class="bubble-row"><div class="avatar">{_e(avatar)}</div><div class="bubble">'
                f'<div class="who">{_e(who)}</div>{_e(text)}</div></div>', unsafe_allow_html=True)


def chips(items: Iterable[str]) -> None:
    st.markdown("".join(f'<span class="chip">{_e(i)}</span>' for i in items), unsafe_allow_html=True)


def escalation_banner(msg: str) -> None:
    st.markdown(f'<div class="escalate">🚨 {_e(msg)}</div>', unsafe_allow_html=True)
