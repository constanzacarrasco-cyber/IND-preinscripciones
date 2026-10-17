"""Punto de entrada del prototipo TICA — IND Región de Aysén.

Ejecutar: streamlit run app.py
"""

import streamlit as st

from ind_app.config import PAGES
from ind_app.screens import home, ind, profesor
from ind_app.styles import load_styles

st.set_page_config(
    page_title="Preinscripción Deportiva | IND Aysén",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="collapsed",
)
load_styles()

if "pagina" not in st.session_state:
    st.session_state["pagina"] = "inicio"

if st.session_state["pagina"] not in PAGES:
    st.session_state["pagina"] = "inicio"

screens = {"inicio": home.render, "profesor": profesor.render, "ind": ind.render}
screens[st.session_state["pagina"]]()
