from __future__ import annotations

import html
import streamlit as st


NAV_ITEMS = [
    ("홈", "⌂"),
    ("시장 현황", "▥"),
    ("종목 분석", "◫"),
    ("공시 분석", "▤"),
    ("테마 & 섹터", "◇"),
    ("포트폴리오", "▣"),
    ("관심 종목", "☆"),
    ("AI 인사이트", "✦"),
    ("데이터 연결 관리", "⚙"),
]


def apply_theme():
    st.markdown(
        """
<style>
:root {
  --bg:#07111f;
  --bg2:#0a1729;
  --surface:#0d1b2e;
  --surface2:#10223a;
  --line:#1d3554;
  --line2:#294766;
  --text:#f4f8ff;
  --muted:#8ea3bd;
  --blue:#3b82f6;
  --blue2:#60a5fa;
  --green:#22c55e;
  --red:#ff4d5e;
  --cyan:#22d3ee;
}
html,body,[class*="css"] {
  font-family:Pretendard,"Noto Sans KR","Apple SD Gothic Neo",sans-serif;
}
.stApp {
  background:radial-gradient(circle at 45% -10%,#102846 0%,var(--bg) 38%,#050c16 100%);
  color:var(--text);
}
.block-container {
  max-width:1500px;
  padding-top:1.1rem;
  padding-bottom:3rem;
}
header[data-testid="stHeader"] {
  background:rgba(7,17,31,.86);
  backdrop-filter:blur(14px);
}
section[data-testid="stSidebar"] {
  background:linear-gradient(180deg,#08172a 0%,#06111f 100%);
  border-right:1px solid var(--line);
}
section[data-testid="stSidebar"] > div { padding-top:.9rem; }
[data-testid="stSidebar"] .stRadio > label { display:none; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] { gap:5px; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
  border-radius:10px;
  padding:.62rem .65rem;
  color:#a9bbd1;
  transition:all .15s ease;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover { background:#102440; color:#fff; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) {
  background:linear-gradient(90deg,#123d78,#102d55);
  color:#fff;
  box-shadow:inset 3px 0 var(--blue),0 5px 18px rgba(0,0,0,.16);
  font-weight:750;
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] { color:#9bb0c8; }

h1,h2,h3,h4 { color:var(--text); letter-spacing:-.035em; }
h1 { font-weight:800; }
h2,h3 { font-weight:760; }
p,li { line-height:1.6; }
[data-testid="stCaptionContainer"] { color:var(--muted); }
[data-testid="stMetric"] {
  background:linear-gradient(145deg,#0f2137,#0b192b);
  border:1px solid var(--line);
  border-radius:14px;
  padding:15px 17px;
  box-shadow:0 10px 28px rgba(0,0,0,.18);
}
[data-testid="stMetricLabel"] { color:var(--muted); }
[data-testid="stMetricValue"] { color:var(--text); font-weight:780; }
[data-testid="stVerticalBlockBorderWrapper"] {
  border-color:var(--line) !important;
  border-radius:14px !important;
  background:rgba(13,27,46,.9);
  box-shadow:0 10px 30px rgba(0,0,0,.16);
}
.stButton > button,.stFormSubmitButton > button {
  border-radius:9px;
  min-height:2.6rem;
  font-weight:700;
  border-color:var(--line2);
  background:#10223a;
  color:#e8f1ff;
}
.stButton > button:hover,.stFormSubmitButton > button:hover { border-color:#3b6da5; }
.stButton > button[kind="primary"],.stFormSubmitButton > button[kind="primary"] {
  background:linear-gradient(135deg,#2563eb,#3b82f6);
  border-color:#3b82f6;
  color:#fff;
}
.stTextInput input,.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] > div {
  border-radius:10px !important;
  background:#0b1b30 !important;
  color:#eef6ff !important;
  border-color:var(--line) !important;
}
.stTextInput input::placeholder,.stTextArea textarea::placeholder { color:#7187a1; }
.stTabs [data-baseweb="tab-list"] { gap:6px; }
.stTabs [data-baseweb="tab"] { border-radius:9px; padding:8px 12px; color:#8ea3bd; }
.stTabs [aria-selected="true"] { background:#12325a; color:#fff; }
.stDataFrame { border:1px solid var(--line); border-radius:12px; overflow:hidden; }

.planx-brand { display:flex; align-items:center; gap:10px; margin:4px 0 22px; }
.planx-brand-mark {
  width:38px; height:38px; border-radius:10px;
  display:flex; align-items:center; justify-content:center;
  background:linear-gradient(145deg,#2563eb,#22a6f2);
  color:white; font-size:20px; font-weight:800;
  box-shadow:0 6px 20px rgba(37,99,235,.25);
}
.planx-brand-title { font-size:19px; line-height:1.15; font-weight:820; letter-spacing:-.03em; color:#f5f9ff; }
.planx-brand-sub { font-size:10px; color:#7890aa; margin-top:3px; }
.planx-hero {
  background:linear-gradient(135deg,#0d1e33 0%,#0b192b 65%,#0b223c 100%);
  border:1px solid var(--line);
  border-radius:18px;
  padding:25px 28px;
  margin-bottom:17px;
  box-shadow:0 14px 38px rgba(0,0,0,.2);
}
.planx-eyebrow { color:#60a5fa; font-size:11px; font-weight:800; letter-spacing:.1em; text-transform:uppercase; margin-bottom:7px; }
.planx-hero h1 { margin:0; font-size:32px; line-height:1.18; }
.planx-hero p { margin:8px 0 0; color:#8ea3bd; font-size:14px; }
.planx-card {
  background:linear-gradient(145deg,#0e2036,#0b192a);
  border:1px solid var(--line);
  border-radius:14px;
  padding:18px 19px;
  min-height:112px;
  box-shadow:0 9px 25px rgba(0,0,0,.17);
}
.planx-card-title { font-size:12px; color:#8ea3bd; margin-bottom:8px; font-weight:700; }
.planx-card-value { font-size:24px; color:#f6faff; font-weight:820; letter-spacing:-.03em; font-variant-numeric:tabular-nums; }
.planx-card-note { margin-top:7px; font-size:11px; color:#7187a1; }
.planx-empty { background:#0c1b2e; border:1px dashed #31506f; border-radius:14px; padding:22px; color:#91a7c0; }
.planx-source { display:inline-flex; align-items:center; gap:5px; color:#91a7c0; background:#0d2035; border:1px solid #294766; padding:4px 8px; border-radius:999px; font-size:10px; }
.planx-status-ok { color:#4ade80; background:#082a20; border-color:#17654c; }
.planx-status-wait { color:#fbbf24; background:#2b2108; border-color:#6b5315; }
.planx-status-bad { color:#ff6b78; background:#2b1015; border-color:#6b202a; }
hr { border-color:var(--line) !important; }

/* Dashboard-style cards and data tables. */
[data-testid="stMarkdownContainer"] table { background:#0b192b; color:#dbeafe; }
[data-testid="stMarkdownContainer"] th { background:#10233b; color:#8ea3bd; border-color:var(--line); }
[data-testid="stMarkdownContainer"] td { border-color:#1a314d; }
[data-testid="stExpander"] { background:#0c1b2e; border-color:var(--line); border-radius:12px; }
[data-testid="stExpander"] summary p { color:#eaf2ff; }
[data-testid="stAlert"] { background:#0d2035; border-color:#284866; color:#dbeafe; }

@media (max-width:900px) {
  .block-container { padding-left:1rem; padding-right:1rem; }
  .planx-hero { padding:21px 20px; }
  .planx-hero h1 { font-size:27px; }
}
@media (max-width:640px) {
  .block-container { padding-top:1rem; }
  .planx-card { min-height:96px; padding:14px; }
  .planx-card-value { font-size:21px; }
}
</style>
""",
        unsafe_allow_html=True,
    )


def brand():
    st.markdown(
        """
<div class="planx-brand">
  <div class="planx-brand-mark">↗</div>
  <div>
    <div class="planx-brand-title">StockDash</div>
    <div class="planx-brand-sub">Data to Insight.</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def hero(title: str, subtitle: str, eyebrow: str = "PLANX INVESTMENT OS"):
    st.markdown(
        f"""
<div class="planx-hero">
  <div class="planx-eyebrow">{html.escape(eyebrow)}</div>
  <h1>{html.escape(title)}</h1>
  <p>{html.escape(subtitle)}</p>
</div>
""",
        unsafe_allow_html=True,
    )


def card(title: str, value: str, note: str = "", status: str = ""):
    status_html = f'<div class="planx-card-note">{html.escape(status)}</div>' if status else ""
    st.markdown(
        f"""
<div class="planx-card">
  <div class="planx-card-title">{html.escape(title)}</div>
  <div class="planx-card-value">{html.escape(value)}</div>
  <div class="planx-card-note">{html.escape(note)}</div>
  {status_html}
</div>
""",
        unsafe_allow_html=True,
    )


def empty_state(title: str, message: str):
    st.markdown(
        f"""
<div class="planx-empty">
  <strong style="color:#e5eefb">{html.escape(title)}</strong><br>
  <span>{html.escape(message)}</span>
</div>
""",
        unsafe_allow_html=True,
    )


def source_badge(label: str, state: str = "wait"):
    cls = {"ok":"planx-status-ok", "bad":"planx-status-bad"}.get(state, "planx-status-wait")
    st.markdown(
        f'<span class="planx-source {cls}">{html.escape(label)}</span>',
        unsafe_allow_html=True,
    )
