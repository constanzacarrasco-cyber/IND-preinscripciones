"""Formulario del profesor conectado a Supabase con RLS. SOLO DATOS FICTICIOS."""
from datetime import date, datetime
from zoneinfo import ZoneInfo
import streamlit as st
from ind_app.backend import cliente
from ind_app.screens.profesor import (validar_rut, normalizar_rut, _formatear_rut,
                                       GENERO_SIGI, CATEGORIAS_SIGI_DEMO, COMUNAS_DEMO)

ZONA = ZoneInfo('America/Coyhaique')


def hoy_local():
    return datetime.now(ZONA).date()


def _abierta(c, hoy):
    return c['publicada'] and date.fromisoformat(c['fecha_apertura']) <= hoy <= date.fromisoformat(c['fecha_cierre'])


def render(perfil, user):
    st.caption('PROTOTIPO ACADÉMICO · PROFESOR/A · VERSIÓN 5')
    st.title('👩‍🏫 Preinscribir deportista')
    st.warning('Solo utiliza datos completamente ficticios. Enviar aquí NO constituye una inscripción oficial en SIGI.')
    if st.button('← Volver al inicio', key='volver_profesor_live'):
        st.session_state['pagina'] = 'inicio'
        st.rerun()
    if st.session_state.pop('prof_live_ok', False):
        st.success('¡Antecedentes de prueba recibidos! El IND podrá revisarlos desde otra sesión.')
    sb = cliente()
    hoy = hoy_local()
    try:
        convocatorias = (sb.table('convocatorias')
                         .select('id,nombre,evento,etapa,fecha_apertura,fecha_cierre,disciplinas,publicada')
                         .order('fecha_cierre').execute().data or [])
    except Exception:
        st.error('No se pudieron consultar las convocatorias. Revisa la conexión o los permisos de la base de datos.')
        return
    if not convocatorias:
        st.info('El IND todavía no ha publicado convocatorias de prueba.')
        return
    convocatoria = st.selectbox('Convocatoria', convocatorias, format_func=lambda c: c['nombre'], key='conv_live')
    abierta = _abierta(convocatoria, hoy)
    a,b,c = st.columns(3)
    a.metric('Apertura', date.fromisoformat(convocatoria['fecha_apertura']).strftime('%d/%m/%Y'))
    b.metric('Cierre', date.fromisoformat(convocatoria['fecha_cierre']).strftime('%d/%m/%Y'))
    c.metric('Estado', 'Abierta' if abierta else 'Cerrada')
    st.caption(f"{convocatoria['evento']} · {convocatoria['etapa']} · Fecha local: {hoy:%d/%m/%Y}")
    if not abierta:
        st.info('La convocatoria está fuera de plazo. Se bloquea el envío.')
    disciplinas = convocatoria.get('disciplinas') or []
    if not disciplinas:
        st.error('Esta convocatoria aún no tiene disciplinas configuradas.')
        return

    # Cada envío utiliza versión distinta para limpiar el formulario automáticamente.
    version = st.session_state.get('form_live_version', 0)
    with st.form(f'form_prof_live_{version}', clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            rut = st.text_input('RUT', placeholder='XX.XXX.XXX-X')
            nombre = st.text_input('Nombre')
            ap = st.text_input('Apellido paterno')
            am = st.text_input('Apellido materno')
            nacimiento = st.date_input('Fecha de nacimiento', value=None,
                                       min_value=date(1900,1,1), max_value=hoy,
                                       format='DD/MM/YYYY')
        with col2:
            genero = st.selectbox('Género (plantilla SIGI)', GENERO_SIGI)
            categoria = st.selectbox('Categoría', CATEGORIAS_SIGI_DEMO)
            disciplina = st.selectbox('Disciplina habilitada', disciplinas)
            establecimiento = st.text_input('Establecimiento (ficticio)')
            comuna = st.selectbox('Comuna', COMUNAS_DEMO)
        confirmo = st.checkbox('Confirmo que utilizo solo datos ficticios de prueba.')
        enviar = st.form_submit_button('Enviar preinscripción de prueba', type='primary',
                                       use_container_width=True, disabled=not abierta)
    if enviar:
        errores=[]
        if not confirmo: errores.append('Debes confirmar que estás utilizando datos ficticios.')
        if not validar_rut(rut): errores.append('RUT inválido: revisa el dígito verificador.')
        for etiqueta, valor in [('Nombre',nombre),('Apellido paterno',ap),('Apellido materno',am),('Establecimiento',establecimiento)]:
            if not valor.strip(): errores.append(f'Completa el campo {etiqueta}.')
        if nacimiento is None: errores.append('Indica fecha de nacimiento.')
        if genero not in ('F','M'): errores.append('Selecciona género.')
        if categoria not in CATEGORIAS_SIGI_DEMO[1:]: errores.append('Selecciona categoría.')
        if comuna not in COMUNAS_DEMO[1:]: errores.append('Selecciona comuna.')
        if not _abierta(convocatoria, hoy): errores.append('El plazo de la convocatoria ya cerró.')
        if errores:
            for error in errores: st.error(error)
        else:
            registro = dict(convocatoria_id=convocatoria['id'], creado_por=user.id,
                            rut=_formatear_rut(rut), rut_normalizado=normalizar_rut(rut),
                            nombre=nombre.strip(),apellido_paterno=ap.strip(),
                            apellido_materno=am.strip(),fecha_nacimiento=nacimiento.isoformat(),
                            genero=genero,categoria=categoria,disciplina=disciplina,
                            establecimiento=establecimiento.strip(),comuna=comuna,estado='pendiente')
            try:
                sb.table('inscripciones').insert(registro).execute()
                st.session_state['form_live_version'] = version + 1
                st.session_state['prof_live_ok'] = True
                st.rerun()
            except Exception as exc:
                codigo = str(exc).lower()
                if '23505' in codigo or 'duplicate' in codigo:
                    st.error('Ya existe un registro con ese RUT y disciplina en la convocatoria.')
                else:
                    st.error('No se pudo guardar el registro. Revisa que la convocatoria siga abierta o consulta al administrador.')

    st.subheader('Mis preinscripciones de prueba')
    try:
        items = (sb.table('inscripciones').select('nombre,apellido_paterno,disciplina,categoria,estado,created_at')
                 .eq('convocatoria_id', convocatoria['id']).eq('creado_por',user.id)
                 .order('created_at',desc=True).limit(100).execute().data or [])
        st.dataframe(items, hide_index=True, use_container_width=True)
    except Exception:
        st.info('No se pudieron cargar las preinscripciones enviadas.')
