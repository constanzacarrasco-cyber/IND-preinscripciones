"""Inicio de sesión verdadero con Supabase Auth. No hay auto-registro público."""
import streamlit as st
from ind_app.backend import cliente


def render():
    st.title('🏅 Sistema de preinscripción deportiva')
    st.caption('IND · Región de Aysén · Prototipo de pruebas')
    st.write('Ingresa con una cuenta de prueba creada por la persona administradora del proyecto.')
    st.warning('**Entorno académico de demostración.** No ingreses RUT ni información real de estudiantes.')
    with st.form('form_login_v5'):
        email = st.text_input('Correo de acceso').strip()
        password = st.text_input('Contraseña', type='password')
        enviar = st.form_submit_button('Ingresar', type='primary')
    if enviar:
        if not email or not password:
            st.error('Ingresa correo y contraseña.')
            return
        try:
            response = cliente().auth.sign_in_with_password({'email': email, 'password': password})
            if not response.user:
                st.error('No se pudo iniciar sesión.')
                return
            st.session_state['pagina'] = 'inicio'
            st.rerun()
        except Exception:
            st.error('No se pudo iniciar sesión. Revisa tus credenciales y que la cuenta esté habilitada.')
