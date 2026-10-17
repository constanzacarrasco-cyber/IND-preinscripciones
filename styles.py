"""Estilo visual de la primera pantalla (sin dependencias externas)."""

import streamlit as st

CSS = """
<style>
    .stApp { background: #f7f9fc; }
    .block-container { max-width: 1120px; padding-top: 2.15rem; padding-bottom: 3.5rem; }
    .eyebrow {font-size:.78rem; font-weight:800; letter-spacing:.10em; color:#187782; text-transform:uppercase;}
    .hero-title {font-size:clamp(2rem,4vw,3.1rem); line-height:1.12; font-weight:800; color:#152b46; margin:.65rem 0 .85rem 0;}
    .hero-copy {font-size:1.08rem; color:#526579; line-height:1.65; max-width:760px;}
    .header-brand {font-size:.95rem; font-weight:800; color:#1c456c;}
    .module-label {font-size:.88rem; font-weight:800; letter-spacing:.06em; color:#147e82;}
    .module-title {font-size:1.45rem; color:#1b354e; font-weight:800; margin:.3rem 0 .7rem 0;}
    .module-body {color:#526579; font-size:.96rem; line-height:1.6; min-height:90px;}
    .step-title {font-weight:800; color:#21364c; font-size:.92rem;}
    .step-sub {color:#596f82; font-size:.87rem; line-height:1.5;}
    .muted {color:#617386; font-size:.9rem;}
    .divider-text {font-weight:800; color:#1b354e; font-size:1.04rem; padding-top:.7rem;}
    .demo-pill {display:inline-block; border-radius:99px; border:1px solid #b9d5d6; background:#e9f5f5; padding:5px 11px; font-weight:750; color:#187782; font-size:.77rem;}
    div.stButton > button {border-radius:12px; min-height:45px; font-weight:700;}
    div[data-testid="stVerticalBlockBorderWrapper"] {border-radius:16px;}
    @media (max-width: 720px) {.block-container{padding-top:1rem;} .module-body{min-height:0;}}
</style>
"""


def load_styles() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
