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
  --bg:#f7f8fa;
  --surface:#ffffff;
  --surface-soft:#f4f6f8;
  --line:#eef0f3;
  --line-strong:#e2e5e9;
  --text:#191f28;
  --muted:#8b95a1;
  --blue:#3182f6;
  --blue-soft:#eef5ff;
  --green:#00a86b;
  --green-soft:#edf9f5;
  --red:#f04452;
  --red-soft:#fff1f2;
  --amber:#d99000;
  --amber-soft:#fff8e6;
}
html,body,[class*="css"] {
  font-family:Pretendard,"Noto Sans KR","Apple SD Gothic Neo",sans-serif;
}
.stApp {
  background:var(--bg);
  color:var(--text);
}
.block-container {
  max-width:1440px;
  padding-top:1.25rem;
  padding-bottom:4rem;
}
header[data-testid="stHeader"] {
  background:rgba(247,248,250,.92);
  backdrop-filter:blur(14px);
}
section[data-testid="stSidebar"] {
  background:#fff;
  border-right:1px solid #f0f1f3;
}
section[data-testid="stSidebar"] > div { padding-top:1rem; }
[data-testid="stSidebar"] .stRadio > label { display:none; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] { gap:3px; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
  border-radius:9px;
  padding:.58rem .65rem;
  color:#66717d;
  transition:background .15s ease,color .15s ease;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
  background:#f5f6f8;
  color:#202832;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) {
  background:#f0f6ff;
  color:#1f6fe5;
  box-shadow:none;
  font-weight:750;
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
  color:#7d8792;
}

h1,h2,h3,h4 { color:var(--text); letter-spacing:-.04em; }
h1 { font-weight:800; }
h2,h3 { font-weight:760; }
p,li { line-height:1.6; }
[data-testid="stCaptionContainer"] { color:var(--muted); }

/* Clean finance-app surfaces */
[data-testid="stMetric"] {
  background:#fff;
  border:1px solid var(--line);
  border-radius:16px;
  padding:16px 18px;
  box-shadow:0 2px 12px rgba(25,31,40,.025);
}
[data-testid="stMetricLabel"] { color:#8b95a1; }
[data-testid="stMetricValue"] { color:#191f28; font-weight:780; letter-spacing:-.025em; }
[data-testid="stVerticalBlockBorderWrapper"] {
  border-color:var(--line) !important;
  border-radius:16px !important;
  background:#fff;
  box-shadow:0 2px 14px rgba(25,31,40,.025);
}
.stButton > button,.stFormSubmitButton > button {
  border-radius:9px;
  min-height:2.6rem;
  font-weight:700;
  border-color:#e2e5e9;
  background:#fff;
  color:#333b46;
  box-shadow:none;
}
.stButton > button:hover,.stFormSubmitButton > button:hover {
  border-color:#c8d9f2;
  background:#f8fbff;
}
.stButton > button[kind="primary"],.stFormSubmitButton > button[kind="primary"] {
  background:#3182f6;
  border-color:#3182f6;
  color:#fff;
  box-shadow:0 4px 10px rgba(49,130,246,.16);
}
.stTextInput input,.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] > div {
  border-radius:12px !important;
  background:#fff !important;
  color:#191f28 !important;
  border:1px solid #e5e8eb !important;
  box-shadow:none !important;
}
.stTextInput input:focus,.stTextArea textarea:focus {
  border-color:#75aaf7 !important;
  box-shadow:0 0 0 3px rgba(49,130,246,.09) !important;
}
.stTextInput input::placeholder,.stTextArea textarea::placeholder { color:#a5adb6; }
.stTabs [data-baseweb="tab-list"] { gap:4px; border-bottom:1px solid #eef0f3; }
.stTabs [data-baseweb="tab"] { border-radius:8px 8px 0 0; padding:9px 13px; color:#8b95a1; }
.stTabs [aria-selected="true"] { color:#3182f6; background:#f7faff; }
.stDataFrame { border:1px solid var(--line); border-radius:12px; overflow:hidden; }

.planx-brand { display:flex; align-items:center; gap:10px; margin:4px 0 24px; }
.planx-brand-mark {
  width:38px; height:38px; border-radius:11px;
  display:flex; align-items:center; justify-content:center;
  background:#3182f6;
  color:#fff; font-size:20px; font-weight:800;
}
.planx-brand-title { font-size:19px; line-height:1.15; font-weight:820; letter-spacing:-.035em; color:#191f28; }
.planx-brand-sub { font-size:10px; color:#9aa3ad; margin-top:3px; }

/* Main home: airy, rounded, information-first */
.planx-hero {
  background:#fff;
  border:1px solid var(--line);
  border-radius:20px;
  padding:28px 30px 27px;
  margin-bottom:15px;
  box-shadow:0 3px 18px rgba(25,31,40,.035);
}
.planx-eyebrow {
  color:#3182f6;
  font-size:10px;
  font-weight:800;
  letter-spacing:.1em;
  text-transform:uppercase;
  margin-bottom:8px;
}
.planx-hero h1 { margin:0; font-size:32px; line-height:1.2; }
.planx-hero p { margin:8px 0 0; color:#7b8591; font-size:14px; }

/* Search form is visually treated as the primary action */
.stForm:has(input[placeholder*="종목명"]) {
  background:#fff;
  border:1px solid #e5e8eb;
  border-radius:14px;
  padding:4px;
  box-shadow:0 4px 18px rgba(25,31,40,.04);
}
.stForm:has(input[placeholder*="종목명"]) input {
  border:0 !important;
  box-shadow:none !important;
}

.planx-card {
  position:relative;
  background:#fff;
  border:1px solid var(--line);
  border-radius:16px;
  padding:18px 19px;
  min-height:110px;
  box-shadow:0 3px 15px rgba(25,31,40,.028);
  transition:transform .15s ease,box-shadow .15s ease;
}
.planx-card:hover {
  transform:translateY(-1px);
  box-shadow:0 7px 22px rgba(25,31,40,.055);
}
.planx-card-title { font-size:12px; color:#8b95a1; margin-bottom:8px; font-weight:650; }
.planx-card-value { font-size:24px; color:#191f28; font-weight:820; letter-spacing:-.035em; font-variant-numeric:tabular-nums; }
.planx-card-note { margin-top:7px; font-size:11px; color:#a0a8b1; }

.planx-empty {
  background:#f8fafc;
  border:1px dashed #dfe4e9;
  border-radius:14px;
  padding:21px;
  color:#7d8792;
}
.planx-source {
  display:inline-flex; align-items:center; gap:5px;
  color:#7b8591;
  background:#f6f7f9;
  border:1px solid #eceef1;
  padding:4px 8px;
  border-radius:999px;
  font-size:10px;
}
.planx-status-ok { color:#00875a; background:#edf9f5; border-color:#c8eee0; }
.planx-status-wait { color:#a76b00; background:#fff8e6; border-color:#f4e2b0; }
.planx-status-bad { color:#d92d3b; background:#fff1f2; border-color:#ffd5d9; }
hr { border-color:#eef0f3 !important; }
[data-testid="stMarkdownContainer"] table { background:#fff; color:#333b46; }
[data-testid="stMarkdownContainer"] th { background:#f8f9fa; color:#7d8792; border-color:#eef0f3; }
[data-testid="stMarkdownContainer"] td { border-color:#f0f1f3; }
[data-testid="stExpander"] { background:#fff; border-color:#e9ebee; border-radius:12px; }
[data-testid="stExpander"] summary p { color:#333b46; }
[data-testid="stAlert"] { background:#f6f9ff; border-color:#dbe9ff; color:#3f4b59; }

@media (max-width:900px) {
  .block-container { padding-left:1rem; padding-right:1rem; }
  .planx-hero { padding:22px 20px; }
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
<div class="planx-empty"><strong style="color:#333b46">{html.escape(title)}</strong><br><span>{html.escape(message)}</span></div>
""", unsafe_allow_html=True)


def source_badge(label: str, state: str = "wait"):
    cls = {"ok":"planx-status-ok", "bad":"planx-status-bad"}.get(state, "planx-status-wait")
    st.markdown(f'<span class="planx-source {cls}">{html.escape(label)}</span>', unsafe_allow_html=True)
