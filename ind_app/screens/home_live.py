"""Pantalla principal tras iniciar sesión con un perfil autorizado."""
import streamlit as st
from ind_app.backend import cerrar_sesion


def render(perfil):
    rol = perfil['role']
    nombre = perfil.get('display_name') or 'Usuario/a'
    st.title('🏅 Preinscripción Deportiva · IND Aysén')
    st.caption('VERSIÓN 5 · PRUEBA MULTIUSUARIO')
    st.write(f'Bienvenido/a, **{nombre}**. Perfil autorizado: **{"IND" if rol == "ind" else "Profesor/a"}**.')
    st.warning('Usar únicamente antecedentes totalmente ficticios. La importación a SIGI no está automatizada.')
    if rol == 'ind':
        st.write('Desde el panel IND podrás crear convocatorias, revisar registros de prueba, validarlos y generar un archivo con el formato de SIGI.')
        if st.button('Entrar al panel IND →', type='primary', use_container_width=True):
            st.session_state['pagina'] = 'ind'
            st.rerun()
    else:
        st.write('Desde el formulario podrás ver convocatorias publicadas y enviar antecedentes ficticios para que sean revisados por el IND.')
        if st.button('Entrar al formulario Profesor/a →', type='primary', use_container_width=True):
            st.session_state['pagina'] = 'profesor'
            st.rerun()
    if st.button('Cerrar sesión', key='logout_home_live'):
        cerrar_sesion()
        st.rerun()
    st.info('**Nueva función:** las inscripciones se conservan en una base de datos de prueba y pueden consultarse desde sesiones distintas, con permisos según el perfil.')
