"""Sistema de preinscripción deportiva IND Aysén - V5.

Si Supabase NO está configurado, se conserva el modo DEMO V4.
Si Supabase está configurado, se exige autenticación y roles reales, con RLS.
"""
import streamlit as st

from ind_app.config import PAGES
from ind_app.styles import load_styles
from ind_app.backend import configurado, usuario_y_perfil, cerrar_sesion
from ind_app.screens import home, ind, profesor, home_live, login, ind_live, profesor_live

st.set_page_config(page_title='Preinscripción Deportiva | IND Aysén',
                   page_icon='🏅', layout='wide', initial_sidebar_state='collapsed')
load_styles()
if st.session_state.get('pagina') not in PAGES:
    st.session_state['pagina']='inicio'

if not configurado():
    st.sidebar.warning('MODO DEMO V4: sin base de datos compartida')
    pantallas={'inicio':home.render,'profesor':profesor.render,'ind':ind.render}
    pantallas[st.session_state['pagina']]()
else:
    user, perfil=usuario_y_perfil()
    if user is None:
        st.session_state['pagina']='inicio'
        login.render()
    elif perfil is None or perfil.get('role') not in ('profesor','ind'):
        st.error('La cuenta no tiene un perfil autorizado. El administrador debe asignar el rol en Supabase.')
        if st.button('Cerrar sesión'):
            cerrar_sesion()
            st.rerun()
    else:
        st.sidebar.caption('PROTOTIPO DE PRUEBAS · IND AYSÉN')
        st.sidebar.write(f"**{perfil.get('display_name') or 'Usuario/a'}**")
        st.sidebar.caption(f"Perfil: {perfil['role']}")
        if st.sidebar.button('Cerrar sesión'):
            cerrar_sesion()
            st.rerun()
        # Control de rutas adicional a las políticas RLS de la base de datos.
        if st.session_state['pagina']=='inicio':
            home_live.render(perfil)
        elif st.session_state['pagina']=='profesor' and perfil['role']=='profesor':
            profesor_live.render(perfil,user)
        elif st.session_state['pagina']=='ind' and perfil['role']=='ind':
            ind_live.render(perfil,user)
        else:
            st.session_state['pagina']='inicio'
            st.rerun()
