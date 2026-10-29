# IND Región de Aysén · Sistema de preinscripción deportiva · V5

Prototipo académico en Streamlit/Python. **Esta versión agrega una opción de base de datos compartida y usuarios por perfil (Supabase), además de mantener intacto el modo de demostración V4.**

> ⚠️ Por ahora usar **solo datos totalmente ficticios**. La aplicación no está autorizada para tratar registros reales de estudiantes ni para ingresar datos en una convocatoria oficial de SIGI. La aceptación de los Excel por SIGI requiere pruebas del IND.

## ¿Qué cambia con V5?

- **Profesor/a autenticado:** visualiza convocatorias publicadas, registra antecedentes de prueba dentro de plazo y consulta solo sus envíos.
- **IND autenticado:** crea convocatorias y fechas; publica o retira convocatorias; revisa registros de todos los profesores; valida registros y genera un Excel en la estructura SIGI existente.
- **Persistencia entre equipos:** los registros se almacenan en Supabase y pueden verse desde otros navegadores. Protegidos por Row Level Security (RLS) y perfiles asignados por administradores.
- **Sin configuración:** la aplicación sigue usando **modo demo V4**, con registros temporales en la misma sesión.

## Instalación SIN riesgo para lo que ya funciona

1. **Haz una copia de respaldo de tu repositorio o conserva el ZIP de V4.**
2. Descomprime el ZIP `IND_V5_ACTUALIZAR_GITHUB.zip`.
3. En GitHub, en tu repositorio `IND-preinscripciones`, entra a la raíz y usa `Add file > Upload files` para subir los archivos y carpetas del ZIP, **conservando la estructura**. Confirma que `app.py` está en la raíz y los nuevos archivos quedan en `ind_app/screens/`.
4. Confirma cambios con `Commit changes`.
5. Regresa a Streamlit: **si aún no configuraste Supabase, V4 debe seguir funcionando igual**. Esto es intencional.

### Estructura V5

```text
app.py
requirements.txt
README.md
.streamlit/config.toml
ind_app/
    backend.py                 (NUEVO)
    config.py
    export_sigi.py
    styles.py
    screens/
        home.py
        home_live.py           (NUEVO)
        login.py               (NUEVO)
        profesor.py            (V4, respaldo)
        profesor_live.py       (NUEVO)
        ind.py                 (V4, respaldo)
        ind_live.py            (NUEVO)
assets/
    plantilla_sigi_blanca.xlsx
supabase/
    setup.sql                  (NUEVO)
PLAN_DE_PRUEBAS.md             (NUEVO)
```

## Conectar la base de datos compartida (cuando ya subiste V5)

Usaremos [Supabase](https://supabase.com/), con una base de datos de **prueba**, distinta de cualquier infraestructura del IND.

**Paso 1.** Crea una cuenta en Supabase y selecciona **New project**. Guarda la contraseña de administración del proyecto fuera de GitHub.

**Paso 2.** En tu proyecto de Supabase, entra a **SQL Editor > New query**. Copia el contenido de `supabase/setup.sql`, pégalo y presiona **Run**. Este archivo crea las tres tablas y las políticas RLS.

**Paso 3.** En Supabase **Authentication > Users**, crea **dos usuarios de prueba** con contraseñas distintas (uno profesor y uno IND). Usa correos controlados por ustedes. Verifica que aparezcan confirmados/habilitados. **Desactiva el registro público de nuevas cuentas** en las opciones de autenticación para que nadie cree usuarios por su cuenta. No coloques las contraseñas en GitHub.

**Paso 4.** Copia los IDs UUID de ambos usuarios desde `Authentication > Users`. Vuelve a **SQL Editor**, sustituye los ejemplos por los UUID reales y ejecuta SOLO estas líneas (con tus propios IDs):

```sql
insert into public.profiles (id, display_name, role)
values
  ('UUID_REAL_DEL_PROFESOR', 'Profesor de prueba', 'profesor'),
  ('UUID_REAL_DEL_IND', 'Funcionario IND de prueba', 'ind')
on conflict (id) do update
set display_name = excluded.display_name, role = excluded.role;
```

**Paso 5.** En Supabase, ve a **Project Settings > API** o al panel de claves del proyecto, y copia **Project URL** y la clave **publishable / anon**. **NO copies `service_role` ni `secret`**.

**Paso 6.** Abre tu aplicación en Streamlit Cloud y entra a **Manage app > Settings > Secrets** (los nombres pueden variar ligeramente), pega este contenido reemplazando los ejemplos:

```toml
[supabase]
url = "https://TU-PROYECTO.supabase.co"
publishable_key = "sb_publishable_TU_CLAVE"
```

Si Supabase ofrece una clave **anon heredada** en vez de `publishable_key`, utiliza:

```toml
[supabase]
url = "https://TU-PROYECTO.supabase.co"
anon_key = "TU_CLAVE_ANON_PUBLICA"
```

Guarda los secretos y reinicia la aplicación. **Jamás subas `secrets.toml`, contraseñas ni claves `service_role` a GitHub.**

**Paso 7.** Se mostrará la pantalla de ingreso con correo y contraseña. Prueba primero con el usuario IND, crea una convocatoria ficticia publicada y luego inicia sesión con el profesor desde otro navegador o ventana privada.

## Guion de demostración

Consulta `PLAN_DE_PRUEBAS.md`. El funcionamiento esperado es:

1. **IND (sesión A):** iniciar sesión y crear una convocatoria de ejemplo con fechas abiertas.
2. **Profesor (sesión B):** iniciar sesión, abrir la convocatoria e ingresar un deportista completamente ficticio.
3. **IND (sesión A):** abrir la sección *Revisar y exportar*, comprobar que aparece el nuevo registro y marcarlo como **validado**.
4. **IND:** descargar Excel y comprobar que conserva la plantilla de SIGI.
5. **IND:** retirar la publicación de la convocatoria. El profesor no podrá iniciar nuevos registros de esa convocatoria.

## Limitaciones importantes

- Esta es una **prueba de concepto multiusuario**, no una implementación institucional aprobada. Se requieren políticas de privacidad, evaluación de seguridad, gestión de respaldos, autorización del IND y pruebas formales antes de usar datos reales.
- El prototipo no integra automáticamente SIGI ni verifica por sí mismo que los registros ya quedaron inscritos en SIGI.
- Las disciplinas son de ejemplo; deben ajustarse al catálogo real del evento y a la plantilla de importación.
- Las opciones SUB 10, SUB 12, SUB 14, SUB 17 provienen de la plantilla recibida, pero no se implementa aún validación de categoría por edad.
- Para cerrar plazos, se comprueba la fecha de **America/Coyhaique**, tanto en la interfaz como en la política de base de datos.
- El administrador crea convocatorias. Un profesor solo puede consultar las publicadas y sus propias inscripciones. Los roles se asignan desde Supabase, nunca desde el formulario público.
- El límite de registros en cada revisión se fijó en 5.000; si más adelante lo superan deberá implementarse paginación.

## Ejecutar localmente

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Si quieres activar Supabase localmente, crea `.streamlit/secrets.toml` con el mismo formato indicado arriba y asegúrate de excluirlo de Git con `.gitignore`.
