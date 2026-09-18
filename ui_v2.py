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
  --bg:#f4f7fb;
  --surface:#ffffff;
  --surface-soft:#f8fafc;
  --line:#e2e8f0;
  --line-strong:#cbd5e1;
  --text:#172033;
  --muted:#718096;
  --blue:#2563eb;
  --blue-soft:#eff6ff;
  --green:#059669;
  --green-soft:#ecfdf5;
  --red:#dc2626;
  --red-soft:#fef2f2;
  --amber:#d97706;
  --amber-soft:#fffbeb;
}
html,body,[class*="css"] { font-family:Pretendard,"Noto Sans KR","Apple SD Gothic Neo",sans-serif; }
.stApp { background:linear-gradient(180deg,#f8fafc 0%,#f3f6fa 100%); color:var(--text); }
.block-container { max-width:1500px; padding-top:1.1rem; padding-bottom:3rem; }
header[data-testid="stHeader"] { background:rgba(248,250,252,.9); backdrop-filter:blur(12px); }
section[data-testid="stSidebar"] { background:#ffffff; border-right:1px solid var(--line); }
section[data-testid="stSidebar"] > div { padding-top:.9rem; }
[data-testid="stSidebar"] .stRadio > label { display:none; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] { gap:4px; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label { border-radius:10px; padding:.62rem .65rem; color:#64748b; transition:all .15s ease; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover { background:#f1f5f9; color:#1e293b; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) { background:#eaf2ff; color:#1d4ed8; box-shadow:inset 3px 0 #2563eb; font-weight:750; }
section[data-testid="stSidebar"] p,section[data-testid="stSidebar"] label,section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] { color:#64748b; }

h1,h2,h3,h4 { color:var(--text); letter-spacing:-.035em; }
h1 { font-weight:800; } h2,h3 { font-weight:760; }
p,li { line-height:1.6; }
[data-testid="stCaptionContainer"] { color:var(--muted); }
[data-testid="stMetric"] { background:#fff; border:1px solid var(--line); border-radius:14px; padding:15px 17px; box-shadow:0 5px 18px rgba(15,23,42,.045); }
[data-testid="stMetricLabel"] { color:var(--muted); }
[data-testid="stMetricValue"] { color:var(--text); font-weight:780; }
[data-testid="stVerticalBlockBorderWrapper"] { border-color:var(--line) !important; border-radius:14px !important; background:#fff; box-shadow:0 5px 18px rgba(15,23,42,.04); }
.stButton > button,.stFormSubmitButton > button { border-radius:9px; min-height:2.6rem; font-weight:700; border-color:#d5dde8; background:#fff; color:#334155; }
.stButton > button:hover,.stFormSubmitButton > button:hover { border-color:#93b4e8; background:#f8fbff; }
.stButton > button[kind="primary"],.stFormSubmitButton > button[kind="primary"] { background:linear-gradient(135deg,#2563eb,#3b82f6); border-color:#2563eb; color:#fff; }
.stTextInput input,.stTextArea textarea,.stSelectbox div[data-baseweb="select"] > div { border-radius:10px !important; background:#fff !important; color:#172033 !important; border-color:#dce3ec !important; }
.stTextInput input::placeholder,.stTextArea textarea::placeholder { color:#94a3b8; }
.stTabs [data-baseweb="tab-list"] { gap:6px; }
.stTabs [data-baseweb="tab"] { border-radius:9px; padding:8px 12px; color:#64748b; }
.stTabs [aria-selected="true"] { background:#eaf2ff; color:#1d4ed8; }
.stDataFrame { border:1px solid var(--line); border-radius:12px; overflow:hidden; }

.planx-brand { display:flex; align-items:center; gap:10px; margin:4px 0 22px; }
.planx-brand-mark { width:38px; height:38px; border-radius:10px; display:flex; align-items:center; justify-content:center; background:linear-gradient(145deg,#2563eb,#60a5fa); color:#fff; font-size:20px; font-weight:800; box-shadow:0 6px 20px rgba(37,99,235,.18); }
.planx-brand-title { font-size:19px; line-height:1.15; font-weight:820; letter-spacing:-.03em; color:#172033; }
.planx-brand-sub { font-size:10px; color:#94a3b8; margin-top:3px; }
.planx-hero { background:linear-gradient(135deg,#fff 0%,#f8fbff 65%,#eef6ff 100%); border:1px solid #dfe7f1; border-radius:18px; padding:25px 28px; margin-bottom:17px; box-shadow:0 8px 28px rgba(15,23,42,.055); }
.planx-eyebrow { color:#2563eb; font-size:11px; font-weight:800; letter-spacing:.1em; text-transform:uppercase; margin-bottom:7px; }
.planx-hero h1 { margin:0; font-size:32px; line-height:1.18; }
.planx-hero p { margin:8px 0 0; color:#718096; font-size:14px; }
.planx-card { background:#fff; border:1px solid #e2e8f0; border-radius:14px; padding:18px 19px; min-height:112px; box-shadow:0 6px 20px rgba(15,23,42,.045); }
.planx-card-title { font-size:12px; color:#718096; margin-bottom:8px; font-weight:700; }
.planx-card-value { font-size:24px; color:#172033; font-weight:820; letter-spacing:-.03em; font-variant-numeric:tabular-nums; }
.planx-card-note { margin-top:7px; font-size:11px; color:#94a3b8; }
.planx-empty { background:#fff; border:1px dashed #cbd5e1; border-radius:14px; padding:22px; color:#64748b; }
.planx-source { display:inline-flex; align-items:center; gap:5px; color:#64748b; background:#f8fafc; border:1px solid #e2e8f0; padding:4px 8px; border-radius:999px; font-size:10px; }
.planx-status-ok { color:#047857; background:#ecfdf5; border-color:#a7f3d0; }
.planx-status-wait { color:#92400e; background:#fffbeb; border-color:#fde68a; }
.planx-status-bad { color:#b91c1c; background:#fef2f2; border-color:#fecaca; }
hr { border-color:#e2e8f0 !important; }
[data-testid="stMarkdownContainer"] table { background:#fff; color:#334155; }
[data-testid="stMarkdownContainer"] th { background:#f8fafc; color:#64748b; border-color:#e2e8f0; }
[data-testid="stMarkdownContainer"] td { border-color:#edf1f5; }
[data-testid="stExpander"] { background:#fff; border-color:#e2e8f0; border-radius:12px; }
[data-testid="stExpander"] summary p { color:#334155; }
[data-testid="stAlert"] { background:#f8fbff; border-color:#dbeafe; color:#334155; }

@media (max-width:900px) { .block-container { padding-left:1rem; padding-right:1rem; } .planx-hero { padding:21px 20px; } .planx-hero h1 { font-size:27px; } }
@media (max-width:640px) { .block-container { padding-top:1rem; } .planx-card { min-height:96px; padding:14px; } .planx-card-value { font-size:21px; } }
</style>
""",
        unsafe_allow_html=True,
    )


def brand():
    st.markdown("""
<div class="planx-brand">
  <div class="planx-brand-mark">↗</div>
  <div><div class="planx-brand-title">StockDash</div><div class="planx-brand-sub">Data to Insight.</div></div>
</div>
""", unsafe_allow_html=True)


def hero(title: str, subtitle: str, eyebrow: str = "PLANX INVESTMENT OS"):
    st.markdown(f"""
<div class="planx-hero"><div class="planx-eyebrow">{html.escape(eyebrow)}</div><h1>{html.escape(title)}</h1><p>{html.escape(subtitle)}</p></div>
""", unsafe_allow_html=True)


def card(title: str, value: str, note: str = "", status: str = ""):
    status_html = f'<div class="planx-card-note">{html.escape(status)}</div>' if status else ""
    st.markdown(f"""
<div class="planx-card"><div class="planx-card-title">{html.escape(title)}</div><div class="planx-card-value">{html.escape(value)}</div><div class="planx-card-note">{html.escape(note)}</div>{status_html}</div>
""", unsafe_allow_html=True)


def empty_state(title: str, message: str):
    st.markdown(f"""
<div class="planx-empty"><strong style="color:#334155">{html.escape(title)}</strong><br><span>{html.escape(message)}</span></div>
""", unsafe_allow_html=True)


def source_badge(label: str, state: str = "wait"):
    cls = {"ok":"planx-status-ok", "bad":"planx-status-bad"}.get(state, "planx-status-wait")
    st.markdown(f'<span class="planx-source {cls}">{html.escape(label)}</span>', unsafe_allow_html=True)
