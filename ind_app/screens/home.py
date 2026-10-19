"""Primera pantalla: bienvenida y selección de perfil (demo sin login)."""

import streamlit as st

from ind_app.config import CAMPOS_INFORMADOS_SIGI, ORG


def _go(page: str) -> None:
    st.session_state["pagina"] = page


def render() -> None:
    st.markdown(f'<div class="header-brand">🏅 {ORG}</div>', unsafe_allow_html=True)
    st.write("")
    st.markdown('<span class="demo-pill">PROTOTIPO ACADÉMICO · TICA</span>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">Sistema de preinscripción deportiva</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="hero-copy">Una propuesta para recibir y validar antecedentes de deportistas, '
        'centralizar solicitudes y preparar archivos compatibles con la importación masiva de SIGI. '
        'El IND mantiene el control de las convocatorias y del registro institucional.</p>',
        unsafe_allow_html=True,
    )
    st.info("🔒 **Versión de demostración:** no ingreses datos reales de estudiantes. Aún no hay autenticación ni almacenamiento seguro.")

    st.markdown('<div class="divider-text">¿Cómo quieres explorar la aplicación?</div>', unsafe_allow_html=True)
    left, right = st.columns(2, gap="large")

    with left:
        with st.container(border=True):
            st.markdown('<div class="module-label">01 · PERFIL EXTERNO</div>', unsafe_allow_html=True)
            st.markdown('<div class="module-title">👩‍🏫 Profesor/a</div>', unsafe_allow_html=True)
            st.markdown(
                '<p class="module-body">Revisar convocatorias habilitadas y, en las próximas etapas, '
                'completar y enviar la información requerida para cada estudiante dentro del plazo establecido.</p>',
                unsafe_allow_html=True,
            )
            st.button("Explorar perfil Profesor/a →", key="go_profesor", type="primary", use_container_width=True, on_click=_go, args=("profesor",))

    with right:
        with st.container(border=True):
            st.markdown('<div class="module-label">02 · PERFIL INTERNO</div>', unsafe_allow_html=True)
            st.markdown('<div class="module-title">🏢 Funcionario/a IND</div>', unsafe_allow_html=True)
            st.markdown(
                '<p class="module-body">En futuras etapas, configurar convocatorias, controlar fechas, '
                'revisar antecedentes y generar el archivo de importación masiva compatible con SIGI.</p>',
                unsafe_allow_html=True,
            )
            st.button("Explorar perfil IND →", key="go_ind", use_container_width=True, on_click=_go, args=("ind",))

    st.markdown('<div class="divider-text">Así funcionará el proceso</div>', unsafe_allow_html=True)
    steps = [
        ("1. IND", "Configura convocatoria y fechas"),
        ("2. Profesor/a", "Entrega los datos requeridos"),
        ("3. Aplicación", "Valida y consolida registros"),
        ("4. IND", "Genera Excel e importa a SIGI"),
    ]
    cols = st.columns(4, gap="small")
    for col, (title, subtitle) in zip(cols, steps):
        with col:
            with st.container(border=True):
                st.markdown(f'<div class="step-title">{title}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="step-sub">{subtitle}</div>', unsafe_allow_html=True)

    with st.expander("Ver los datos de inscripción informados por el IND"):
        st.write("Campos comunicados en la reunión, pendientes de verificar con la plantilla SIGI:")
        for name in CAMPOS_INFORMADOS_SIGI:
            st.markdown(f"- {name}")
        st.caption("El archivo final deberá respetar el orden, formato, nombres y demás reglas reales de la plantilla de SIGI.")
    st.caption("Proyecto universitario · IND Región de Aysén · Primera versión: pantalla de inicio y navegación demostrativa.")
