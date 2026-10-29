"""Conexión Supabase, aislada por sesión de Streamlit.

No incluye clave service_role: las operaciones respetan RLS.
La app V4 sigue funcionando si no hay secretos de Supabase.
"""
import streamlit as st


def configurado() -> bool:
    try:
        cfg = st.secrets.get('supabase', {})
        return bool(cfg.get('url') and (cfg.get('publishable_key') or cfg.get('anon_key')))
    except Exception:
        return False


def cliente():
    if not configurado():
        raise RuntimeError('No está configurada la base de datos compartida.')
    if 'sb_client_v5' not in st.session_state:
        from supabase import create_client
        cfg = st.secrets['supabase']
        key = cfg.get('publishable_key') or cfg.get('anon_key')
        st.session_state['sb_client_v5'] = create_client(cfg['url'], key)
    return st.session_state['sb_client_v5']


def usuario_y_perfil():
    """Retorna (usuario autenticado, perfil), o (None, None)."""
    if 'sb_client_v5' not in st.session_state:
        return None, None
    try:
        sb = cliente()
        res = sb.auth.get_user()
        user = getattr(res, 'user', None)
        if user is None:
            return None, None
        consulta = sb.table('profiles').select('id,role,display_name').eq('id', user.id).limit(1).execute()
        perfiles = consulta.data or []
        return user, perfiles[0] if perfiles else None
    except Exception:
        return None, None


def cerrar_sesion():
    if 'sb_client_v5' in st.session_state:
        try:
            st.session_state['sb_client_v5'].auth.sign_out()
        except Exception:
            pass
        del st.session_state['sb_client_v5']
    st.session_state['pagina'] = 'inicio'
