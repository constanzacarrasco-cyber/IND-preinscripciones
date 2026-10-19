"""Vista de destino de la navegación. El formulario se añadirá en la siguiente etapa."""

import streamlit as st


def render() -> None:
    st.caption("PROTOTIPO ACADÉMICO · PERFIL PROFESOR/A")
    st.title("👩‍🏫 Portal de profesores")
    st.write("Aquí podrás consultar las convocatorias habilitadas y enviar antecedentes de estudiantes.")
    st.info("**Próxima etapa:** formulario de preinscripción con los nueve campos informados por el IND, validación de RUT y control de plazos.")
    st.warning("Todavía no es posible ingresar ni enviar datos. No hay convocatorias reales cargadas.")
    st.button("← Volver al inicio", key="back_profesor", on_click=_back)


def _back() -> None:
    st.session_state["pagina"] = "inicio"
