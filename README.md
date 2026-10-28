# Sistema de preinscripción deportiva IND Aysén — V4

Prototipo académico TICA con Streamlit/Python. **No usar RUT ni datos reales**: la aplicación no dispone de autenticación, almacenamiento institucional ni controles para datos personales. Los registros existen solo en la sesión temporal del navegador.

## Archivos principales

- `app.py`: entrada a Streamlit.
- `ind_app/screens/profesor.py`: formulario de prueba, validación de RUT y fechas.
- `ind_app/screens/ind.py`: revisión de registros en la misma sesión y descarga.
- `ind_app/export_sigi.py`: generador de XLSX que parte de una plantilla vacía.
- `assets/plantilla_sigi_blanca.xlsx`: copia de la plantilla sin datos de estudiantes.
- `requirements.txt`: Streamlit y openpyxl.

## Cómo probar

1. Publica los archivos en GitHub conservando las rutas. En Streamlit Cloud, `app.py` debe ser el punto de entrada y la rama debe ser `main`.
2. En la misma pestaña del navegador, entra a Profesor/a, selecciona la convocatoria de prueba abierta y registra un estudiante completamente ficticio. No utilices información de un alumno real.
3. Vuelve a inicio y entra a IND. Allí aparecerá el registro de prueba solamente en tu sesión. Márcalo «Validado».
4. Descarga el archivo `preinscripciones_DEMO_para_verificar_SIGI.xlsx`.
5. Verifica que conserva la hoja `datos`, las dos filas de encabezados y la hoja `Options`. La importación efectiva debe comprobarla el IND en un entorno autorizado antes de afirmar compatibilidad operativa.

## Límites de esta versión

- **No** hay usuarios, contraseñas, base de datos ni registros compartidos entre navegadores.
- **No** hay conexión, importación automática ni escritura hacia SIGI.
- La selección de deportes y convocatorias utiliza datos de ejemplo; no son eventos reales del IND.
- El diseño sigue en desarrollo. Deben validarse los formatos de fechas y RUT, los catálogos de disciplinas y el archivo con la plataforma institucional.

## Ejecutar localmente

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```
