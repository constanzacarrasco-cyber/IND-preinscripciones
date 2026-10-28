"""Módulo Profesor/a: preinscripción académica de demostración.

IMPORTANTE:
- No usar RUT ni antecedentes reales de estudiantes.
- Los registros se guardan SOLO en st.session_state (sin base de datos).
- No existe autenticación, ni recepción institucional, ni conexión con SIGI.
- Las convocatorias y los catálogos son ficticios para probar la interfaz.
"""

import re
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

import streamlit as st


# Para respetar el calendario de Aysén aunque el servidor esté en otro país.
ZONA_HORARIA = ZoneInfo("America/Santiago")
COMUNAS_DEMO = (
    "Seleccionar comuna",
    "Aysén",
    "Chile Chico",
    "Cisnes",
    "Cochrane",
    "Coyhaique",
    "Guaitecas",
    "Lago Verde",
    "O'Higgins",
    "Río Ibáñez",
    "Tortel",
)
DISCIPLINAS_DEMO = (
    "Seleccionar disciplina",
    "Atletismo",
    "Baloncesto",
    "Fútbol",
    "Voleibol",
)
GENERO_SIGI = ("Seleccionar género", "F", "M")
CATEGORIAS_SIGI_DEMO = (
    "Seleccionar categoría",
    "SUB 10", "SUB 12", "SUB 14", "SUB 17",
)


def _hoy_aysen() -> date:
    return datetime.now(ZONA_HORARIA).date()


def _convocatorias_de_prueba(hoy: date) -> list[dict]:
    """Convocatorias ficticias con una abierta y otra cerrada, siempre comprobables."""
    return [
        {
            "id": "demo-abierta",
            "nombre": "Convocatoria de PRUEBA · Abierta",
            "evento": "Evento deportivo ficticio",
            "etapa": "Etapa regional (demostración)",
            "desde": hoy - timedelta(days=7),
            "hasta": hoy + timedelta(days=14),
        },
        {
            "id": "demo-cerrada",
            "nombre": "Convocatoria de PRUEBA · Cerrada",
            "evento": "Evento de prueba finalizado",
            "etapa": "Etapa comunal (demostración)",
            "desde": hoy - timedelta(days=30),
            "hasta": hoy - timedelta(days=1),
        },
    ]


def _abierta(convocatoria: dict, hoy: date) -> bool:
    return convocatoria["desde"] <= hoy <= convocatoria["hasta"]


def normalizar_rut(rut: str) -> str:
    """Quita puntos, guion y espacios y pasa el dígito verificador a mayúscula."""
    return re.sub(r"[.\-\s]", "", str(rut)).upper()


def validar_rut(rut: str) -> bool:
    """Comprueba el dígito verificador del RUN/RUT chileno (módulo 11)."""
    limpio = normalizar_rut(rut)
    if len(limpio) < 2 or len(limpio) > 10:
        return False
    cuerpo, dv = limpio[:-1], limpio[-1]
    if not cuerpo.isdigit() or not (dv.isdigit() or dv == "K"):
        return False
    if int(cuerpo) == 0:
        return False
    total = sum(int(digito) * (2 + indice % 6) for indice, digito in enumerate(reversed(cuerpo)))
    resultado = 11 - (total % 11)
    esperado = "0" if resultado == 11 else "K" if resultado == 10 else str(resultado)
    return dv == esperado


def _formatear_rut(rut: str) -> str:
    limpio = normalizar_rut(rut)
    cuerpo, dv = limpio[:-1], limpio[-1]
    return f"{int(cuerpo):,}".replace(",", ".") + "-" + dv


def _validar_registro(datos: dict, convocatoria: dict, hoy: date, existentes: list[dict]) -> list[str]:
    errores = []
    if not _abierta(convocatoria, hoy):
        errores.append("La convocatoria está cerrada. No se aceptan nuevos envíos de prueba.")
    if not validar_rut(datos["rut"]):
        errores.append("El RUT es inválido. Revisa el número y su dígito verificador.")
    for campo, etiqueta in [
        ("nombre", "Nombre"),
        ("apellido_paterno", "Apellido paterno"),
        ("apellido_materno", "Apellido materno"),
        ("establecimiento", "Establecimiento"),
    ]:
        if not str(datos[campo]).strip():
            errores.append(f"El campo «{etiqueta}» es obligatorio en esta prueba.")
    fecha = datos["fecha_nacimiento"]
    if not isinstance(fecha, date):
        errores.append("Debes indicar la fecha de nacimiento.")
    elif fecha > hoy or fecha < date(1900, 1, 1):
        errores.append("La fecha de nacimiento está fuera del rango permitido.")
    if datos["genero"] not in {"F", "M"}:
        errores.append("Selecciona el género según las opciones de la plantilla informada por el IND.")
    if datos["categoria"] not in CATEGORIAS_SIGI_DEMO[1:]:
        errores.append("Selecciona una categoría indicada por la plantilla SIGI.")
    if datos["disciplina"] not in DISCIPLINAS_DEMO[1:]:
        errores.append("Selecciona una disciplina deportiva.")
    if datos["comuna"] not in COMUNAS_DEMO[1:]:
        errores.append("Selecciona una comuna.")
    if validar_rut(datos["rut"]):
        rut_limpio = normalizar_rut(datos["rut"])
        if any(
            item["convocatoria_id"] == convocatoria["id"]
            and item["rut_limpio"] == rut_limpio
            and item["disciplina"] == datos["disciplina"]
            for item in existentes
        ):
            errores.append("Ya existe un registro de prueba con ese RUT y disciplina en esta convocatoria.")
    return errores


def _volver() -> None:
    st.session_state["pagina"] = "inicio"


def render() -> None:
    hoy = _hoy_aysen()
    st.caption("PROTOTIPO ACADÉMICO · PERFIL PROFESOR/A · VERSIÓN 4")
    st.title("🏅 Preinscripción de deportistas")
    st.write(
        "En este módulo, el profesor entrega los antecedentes de sus estudiantes. "
        "En esta demostración podrás consultar los registros desde el perfil IND en la misma sesión y descargar un Excel de prueba. No se realiza ninguna inscripción oficial."
    )
    st.warning(
        "🔒 **DEMOSTRACIÓN:** utiliza únicamente datos completamente ficticios. "
        "No hay inicio de sesión, base de datos protegida ni conexión con SIGI. "
        "El botón de registro no envía información al IND."
    )
    st.button("← Volver al inicio", key="back_profesor", on_click=_volver)

    if "prof_registros_demo" not in st.session_state:
        st.session_state["prof_registros_demo"] = []
    if "prof_form_version" not in st.session_state:
        st.session_state["prof_form_version"] = 1
    if "prof_last_message" in st.session_state:
        st.success(st.session_state.pop("prof_last_message"))

    st.subheader("1. Consulta la convocatoria")
    convocatorias = _convocatorias_de_prueba(hoy)
    convocatoria = st.selectbox(
        "Selecciona una convocatoria ficticia",
        options=convocatorias,
        format_func=lambda c: c["nombre"],
        key="prof_convocatoria_demo",
    )
    abierta = _abierta(convocatoria, hoy)
    c1, c2, c3 = st.columns(3)
    c1.metric("Inicio", convocatoria["desde"].strftime("%d/%m/%Y"))
    c2.metric("Cierre", convocatoria["hasta"].strftime("%d/%m/%Y"))
    c3.metric("Estado", "Abierta" if abierta else "Cerrada")
    st.caption(f"{convocatoria['evento']} · {convocatoria['etapa']} · Fecha en Chile: {hoy:%d/%m/%Y}")
    if not abierta:
        st.error("Esta convocatoria de prueba está cerrada. El envío queda bloqueado.")
    else:
        st.info("Convocatoria de prueba abierta. Los datos validados se guardarán **solo en esta sesión del navegador**.")

    st.subheader("2. Ingresa los antecedentes del estudiante")
    st.caption(
        "Se incorporaron los diez campos de la hoja «datos» de la plantilla de importación "
        "entregada por Graciela. Categorías y disciplinas siguen sujetas a validación por convocatoria."
    )
    version = st.session_state["prof_form_version"]
    with st.form(f"form_inscripcion_profesor_{version}", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            rut = st.text_input("RUT", placeholder="Formato: XX.XXX.XXX-X", key=f"rut_{version}")
            nombre = st.text_input("Nombre", key=f"nombre_{version}")
            apellido_paterno = st.text_input("Apellido paterno", key=f"ap_{version}")
            apellido_materno = st.text_input("Apellido materno", key=f"am_{version}")
            fecha_nacimiento = st.date_input(
                "Fecha de nacimiento",
                value=None,
                min_value=date(1900, 1, 1),
                max_value=hoy,
                format="DD/MM/YYYY",
                key=f"nac_{version}",
            )
        with col2:
            genero = st.selectbox("Género (según plantilla SIGI)", GENERO_SIGI, key=f"gen_{version}")
            categoria = st.selectbox(
                "Categoría · referencia de la plantilla SIGI",
                CATEGORIAS_SIGI_DEMO,
                key=f"cat_{version}",
            )
            disciplina = st.selectbox(
                "Disciplina deportiva · catálogo ficticio",
                DISCIPLINAS_DEMO,
                key=f"disc_{version}",
            )
            establecimiento = st.text_input(
                "Establecimiento educacional",
                placeholder="Escribe un establecimiento ficticio",
                key=f"est_{version}",
            )
            comuna = st.selectbox("Comuna", COMUNAS_DEMO, key=f"com_{version}")

        acepto_prueba = st.checkbox(
            "Confirmo que todos los datos que ingresaré son ficticios y solo para probar el prototipo.",
            key=f"acepto_{version}",
        )
        enviado = st.form_submit_button(
            "Validar y registrar en la demostración",
            type="primary",
            use_container_width=True,
            disabled=not abierta,
        )

    if enviado:
        datos = {
            "rut": rut.strip(),
            "nombre": nombre.strip(),
            "apellido_paterno": apellido_paterno.strip(),
            "apellido_materno": apellido_materno.strip(),
            "fecha_nacimiento": fecha_nacimiento,
            "genero": genero,
            "categoria": categoria,
            "disciplina": disciplina,
            "establecimiento": establecimiento.strip(),
            "comuna": comuna,
        }
        errores = _validar_registro(datos, convocatoria, hoy, st.session_state["prof_registros_demo"])
        if not acepto_prueba:
            errores.insert(0, "Debes confirmar que estás usando datos completamente ficticios.")
        if errores:
            st.error("No se pudo registrar la preinscripción de demostración:")
            for error in errores:
                st.markdown(f"- {error}")
        else:
            registro = {
                **datos,
                "rut": _formatear_rut(datos["rut"]),
                "rut_limpio": normalizar_rut(datos["rut"]),
                "convocatoria_id": convocatoria["id"],
                "convocatoria_nombre": convocatoria["nombre"],
                "estado": "Recibido en demostración (NO inscrito en SIGI)",
            }
            st.session_state["prof_registros_demo"].append(registro)
            st.session_state["prof_form_version"] += 1
            st.session_state["prof_last_message"] = (
                "Registro de prueba recibido dentro de esta sesión. "
                "Esto NO constituye una inscripción oficial en SIGI ni un envío al IND."
            )
            st.rerun()

    st.subheader("3. Registros de demostración en esta sesión")
    registros = st.session_state["prof_registros_demo"]
    st.metric("Total de registros de prueba", len(registros))
    if registros:
        vista = [
            {
                "Convocatoria": r["convocatoria_nombre"],
                "Nombre ficticio": f"{r['nombre']} {r['apellido_paterno']}",
                "Categoría": r["categoria"],
                "Disciplina": r["disciplina"],
                "Comuna": r["comuna"],
                "Estado": "Recibido (demo)",
            }
            for r in registros
        ]
        st.dataframe(vista, use_container_width=True, hide_index=True)
        st.button(
            "Eliminar todos los registros de esta sesión",
            key="limpiar_prof_demo",
            on_click=lambda: st.session_state.update({"prof_registros_demo": []}),
        )
    else:
        st.caption("Aún no hay registros ficticios. Completa el formulario para probarlo.")
    st.caption(
        "Versión 4: panel IND y generación de Excel respetando la hoja «datos» y sus dos filas "
        "de encabezados. El formato de importación aún deberá probarse con el IND."
    )
