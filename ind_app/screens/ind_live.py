"""Administración del IND conectada a Supabase con RLS. SOLO PRUEBAS."""
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
import streamlit as st
from ind_app.backend import cliente
from ind_app.export_sigi import generar_excel_sigi

ZONA = ZoneInfo('America/Coyhaique')
DISCIPLINAS_SUGERIDAS = ['Atletismo','Baloncesto','Fútbol','Voleibol']
CATEGORIAS = ['SUB 10','SUB 12','SUB 14','SUB 17']


def render(perfil, user):
    st.caption('PROTOTIPO ACADÉMICO · ADMINISTRADOR IND · VERSIÓN 5')
    st.title('🏢 Panel de preinscripciones')
    st.warning('Demostración con datos ficticios. No se realiza importación automática en SIGI.')
    if st.button('← Volver al inicio',key='volver_ind_live'):
        st.session_state['pagina'] = 'inicio'
        st.rerun()
    sb=cliente()
    hoy=datetime.now(ZONA).date()
    tab_config, tab_revision = st.tabs(['📅 Convocatorias','📋 Revisar y exportar'])

    with tab_config:
        st.subheader('Crear convocatoria de prueba')
        with st.form('new_conv_v5',clear_on_submit=True):
            nombre=st.text_input('Nombre de convocatoria',placeholder='Ejemplo: Prueba escolar 2026')
            evento=st.text_input('Evento configurado en SIGI (descripción de prueba)')
            etapa=st.text_input('Etapa',placeholder='Comunal, regional...')
            disciplinas=st.multiselect('Disciplinas habilitadas (catálogo de ejemplo)',DISCIPLINAS_SUGERIDAS,default=DISCIPLINAS_SUGERIDAS)
            a,b=st.columns(2)
            apertura=a.date_input('Apertura',value=hoy,format='DD/MM/YYYY')
            cierre=b.date_input('Cierre',value=hoy+timedelta(days=14),format='DD/MM/YYYY')
            cupo=st.number_input('Cantidad planificada (orientativa)',min_value=0,value=0,step=1,
                                 help='0 significa sin referencia definida. No bloquea envíos.')
            publicar=st.checkbox('Publicar inmediatamente para profesores de prueba',value=True)
            guardar=st.form_submit_button('Crear convocatoria',type='primary')
        if guardar:
            if not nombre.strip() or not evento.strip() or not etapa.strip():
                st.error('Completa nombre, evento y etapa.')
            elif not disciplinas:
                st.error('Selecciona al menos una disciplina.')
            elif cierre<apertura:
                st.error('El cierre no puede ser anterior a la apertura.')
            else:
                try:
                    sb.table('convocatorias').insert(dict(nombre=nombre.strip(),evento=evento.strip(),
                         etapa=etapa.strip(),disciplinas=disciplinas,
                         fecha_apertura=apertura.isoformat(),fecha_cierre=cierre.isoformat(),
                         cupo_planeado=int(cupo) or None,publicada=publicar,creada_por=user.id)).execute()
                    st.success('Convocatoria de prueba creada.')
                except Exception:
                    st.error('No se pudo crear. Revisa los permisos del usuario IND y la conexión.')
        try:
            convocatorias=(sb.table('convocatorias').select('*').order('created_at',desc=True)
                           .limit(100).execute().data or [])
        except Exception:
            st.error('No se pudieron consultar las convocatorias. ¿Se ejecutó el SQL de instalación?')
            return
        if convocatorias:
            st.subheader('Convocatorias existentes')
            st.dataframe([{k:c[k] for k in ('nombre','evento','etapa','fecha_apertura','fecha_cierre','publicada','cupo_planeado')}
                          for c in convocatorias],hide_index=True,use_container_width=True)
            sel=st.selectbox('Selecciona una convocatoria para publicar / despublicar',convocatorias,
                             format_func=lambda c: c['nombre'],key='ind_cfg_sel')
            texto='Retirar publicación' if sel['publicada'] else 'Publicar convocatoria'
            if st.button(texto,key='ind_publicar',type='secondary'):
                try:
                    sb.table('convocatorias').update({'publicada':not sel['publicada']}).eq('id',sel['id']).execute()
                    st.success('Estado de publicación actualizado.')
                    st.rerun()
                except Exception:
                    st.error('No se pudo actualizar la convocatoria.')
        else:
            st.info('Todavía no hay convocatorias. Crea una para comenzar las pruebas.')

    with tab_revision:
        st.subheader('Registros recibidos')
        if st.button('🔄 Actualizar registros',key='refresh_ind_live'):
            st.rerun()
        if not convocatorias:
            st.info('Primero crea una convocatoria.')
            return
        conv=st.selectbox('Convocatoria a revisar',convocatorias,format_func=lambda c:c['nombre'],key='ind_revision_conv')
        try:
            registros=(sb.table('inscripciones').select('*').eq('convocatoria_id',conv['id'])
                       .order('created_at',desc=True).limit(5000).execute().data or [])
        except Exception:
            st.error('No se pudieron consultar los registros.')
            return
        n_pend=sum(r['estado']=='pendiente' for r in registros)
        n_val=sum(r['estado']=='validado' for r in registros)
        a,b,c=st.columns(3)
        a.metric('Recibidos',len(registros))
        b.metric('Pendientes',n_pend)
        c.metric('Validados',n_val)
        if conv.get('cupo_planeado'):
            limite=conv['cupo_planeado']
            if len(registros)>limite:
                st.warning(f'⚠️ Se recibieron {len(registros)} solicitudes, {len(registros)-limite} por encima de la cantidad planificada ({limite}). Se trata de una alerta, no de un rechazo automático.')
            else:
                st.caption(f'Cantidad orientativa planificada: {limite}. Solicitudes recibidas: {len(registros)}.')
        if not registros:
            st.info('Aún no hay preinscripciones de prueba para esta convocatoria.')
            return
        st.dataframe([dict(Estudiante=f"{r['nombre']} {r['apellido_paterno']}",
                            Disciplina=r['disciplina'],Categoría=r['categoria'],
                            Establecimiento=r['establecimiento'],Comuna=r['comuna'],Estado=r['estado'])
                      for r in registros], hide_index=True,use_container_width=True)
        elegido=st.selectbox('Registro para revisión',registros,
                 format_func=lambda r:f"{r['nombre']} {r['apellido_paterno']} · {r['disciplina']} · {r['estado']}",
                 key='ind_reg_sel')
        with st.expander('Ver datos del registro ficticio',expanded=True):
            st.write({k:elegido.get(k) for k in ('rut','nombre','apellido_paterno','apellido_materno',
                      'fecha_nacimiento','genero','categoria','disciplina','establecimiento','comuna','estado')})
        col1,col2=st.columns(2)
        if col1.button('✓ Marcar validado',type='primary',use_container_width=True):
            try:
                sb.table('inscripciones').update({'estado':'validado'}).eq('id',elegido['id']).execute()
                st.rerun()
            except Exception:
                st.error('No se pudo validar el registro.')
        if col2.button('↺ Devolver a pendiente',use_container_width=True):
            try:
                sb.table('inscripciones').update({'estado':'pendiente'}).eq('id',elegido['id']).execute()
                st.rerun()
            except Exception:
                st.error('No se pudo cambiar el estado.')
        st.subheader('Generación de Excel para SIGI')
        listos=[r for r in registros if r['estado']=='validado']
        st.caption(f'Solo se incluyen registros validados. Cantidad: {len(listos)}. Se preservan las hojas y los dos encabezados de la plantilla entregada por el IND.')
        if not listos:
            st.info('Valida al menos una preinscripción ficticia para generar el Excel.')
        else:
            try:
                # Supabase entrega fechas como ISO (AAAA-MM-DD); exportador recibe date.
                filas=[{**r,'fecha_nacimiento':date.fromisoformat(r['fecha_nacimiento'])} for r in listos]
                xlsx=generar_excel_sigi(filas)
                st.download_button('⬇️ Descargar archivo XLSX en formato SIGI',data=xlsx,
                                   file_name='preinscripciones_PRUEBA_SIGI.xlsx',
                                   mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                   type='primary',use_container_width=True)
            except Exception:
                st.error('No se pudo generar el archivo. Revisa la plantilla o los datos recibidos.')
        st.warning('El archivo generado todavía requiere una prueba institucional autorizada en SIGI. NO importes datos ficticios en una convocatoria oficial.')
