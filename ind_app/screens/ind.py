"""Vista de destino demostrativa. Sin acceso real ni administración todavía."""

import streamlit as st


def render() -> None:
    st.caption("PROTOTIPO ACADÉMICO · PERFIL IND")
    st.title("🏢 Panel del IND")
    st.write("Este módulo permitirá configurar convocatorias y preparar archivos para la importación masiva en SIGI.")
    st.info("**Próxima etapa:** configuración de eventos, fechas, disciplinas y revisión de registros.")
    st.warning("Acceso de demostración: **no representa una autenticación institucional**. No permite importar datos en SIGI.")
    st.button("← Volver al inicio", key="back_ind", on_click=_back)


def _back() -> None:
    st.session_state["pagina"] = "inicio"
