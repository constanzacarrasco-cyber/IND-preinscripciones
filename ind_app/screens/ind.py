"""Panel IND de demostración: revisión y exportación de registros en sesión.

Advertencia: no hay autenticación ni base de datos compartida. Los registros
solo existen en st.session_state del mismo navegador/sesión; no utilizar
información real de menores o estudiantes.
"""
import streamlit as st

from ind_app.export_sigi import generar_excel_sigi


def _volver() -> None:
    st.session_state["pagina"] = "inicio"


def render() -> None:
    st.caption("PROTOTIPO ACADÉMICO · PERFIL IND · VERSIÓN 4")
    st.title("🏢 Panel de revisión del IND")
    st.write("Consulta los registros ficticios del formulario Profesor/a y genera un archivo de prueba con el formato de SIGI.")
    st.warning(
        "🔒 **DEMO SIN AUTENTICACIÓN NI BASE DE DATOS COMPARTIDA.** "
        "Este panel muestra únicamente datos ficticios capturados en **esta misma sesión del navegador**. "
        "No recibe registros de otros profesores ni comunica nada al IND o a SIGI."
    )
    st.button("← Volver al inicio", on_click=_volver, key="back_ind")
    registros = st.session_state.setdefault("prof_registros_demo", [])

    st.subheader("1. Resumen de preinscripciones de prueba")
    pendientes = sum(r.get("revision_demo") != "Validado" for r in registros)
    aprobados = len(registros) - pendientes
    col1, col2, col3 = st.columns(3)
    col1.metric("Recibidas", len(registros))
    col2.metric("Pendientes de revisión", pendientes)
    col3.metric("Validadas", aprobados)

    if not registros:
        st.info(
            "Aún no hay registros en esta sesión. Vuelve al inicio → Perfil Profesor/a, "
            "registra un deportista completamente ficticio y regresa a este panel sin cerrar la sesión."
        )
        return

    nombres_convocatorias = sorted({r["convocatoria_nombre"] for r in registros})
    nombre_convocatoria = st.selectbox(
        "Convocatoria a revisar", nombres_convocatorias, key="ind_convocatoria_filtro"
    )
    indices = [i for i, r in enumerate(registros) if r["convocatoria_nombre"] == nombre_convocatoria]
    tabla = [
        {
            "N.º": i + 1,
            "Estudiante ficticio": f"{registros[i]['nombre']} {registros[i]['apellido_paterno']}",
            "Disciplina": registros[i]["disciplina"],
            "Categoría": registros[i]["categoria"],
            "Estado revisión": registros[i].get("revision_demo", "Pendiente"),
        }
        for i in indices
    ]
    st.dataframe(tabla, hide_index=True, use_container_width=True)

    st.subheader("2. Revisión administrativa (simulada)")
    fila = st.selectbox(
        "Selecciona un registro para revisar",
        indices,
        format_func=lambda i: (
            f"{registros[i]['nombre']} {registros[i]['apellido_paterno']} "
            f"— {registros[i]['disciplina']}"
        ),
    )
    r = registros[fila]
    with st.expander("Ver los diez campos de la planilla SIGI", expanded=True):
        st.write({
            "RUT (ficticio)": r["rut"],
            "Nombre": r["nombre"],
            "Apellido paterno": r["apellido_paterno"],
            "Apellido materno": r["apellido_materno"],
            "Fecha de nacimiento": r["fecha_nacimiento"].strftime("%d/%m/%Y"),
            "Género": r["genero"],
            "Categoría": r["categoria"],
            "Disciplina": r["disciplina"],
            "Establecimiento": r["establecimiento"],
            "Comuna": r["comuna"],
        })
    a, b = st.columns(2)
    if a.button("✓ Validar para exportación de prueba", type="primary", use_container_width=True):
        registros[fila]["revision_demo"] = "Validado"
        st.success("Registro ficticio validado para la exportación de demostración.")
        st.rerun()
    if b.button("↺ Volver a pendiente", use_container_width=True):
        registros[fila]["revision_demo"] = "Pendiente"
        st.rerun()

    st.subheader("3. Descargar Excel de demostración")
    listos = [registros[i] for i in indices if registros[i].get("revision_demo") == "Validado"]
    st.caption(
        "La descarga usa la hoja «datos» de la plantilla proporcionada por Graciela, "
        "preserva sus dos filas de encabezados y la hoja auxiliar «Options»."
    )
    if not listos:
        st.info("Primero valida al menos un registro ficticio de esta convocatoria.")
        return
    try:
        archivo = generar_excel_sigi(listos)
    except (ValueError, FileNotFoundError, KeyError) as exc:
        st.error(f"No se pudo preparar el archivo: {exc}")
        return
    st.download_button(
        "⬇️ Descargar planilla de prueba compatible en estructura con SIGI",
        data=archivo,
        file_name="preinscripciones_DEMO_para_verificar_SIGI.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary",
        use_container_width=True,
    )
    st.warning(
        "Este archivo **no ha sido validado mediante una importación real en SIGI**. "
        "No lo importes en una convocatoria oficial sin autorización y pruebas del IND."
    )
