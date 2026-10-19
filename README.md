# Prototipo Streamlit — Preinscripciones Deportivas IND Aysén

**Entrega 01:** estructura del proyecto y primera pantalla de bienvenida con dos perfiles de demostración.

> **Atención:** este es un prototipo académico. No tiene autenticación, autorización, base de datos ni medidas suficientes para operar con datos personales reales. **Usar únicamente información ficticia.**

## Estructura

```text
IND_Preinscripciones_Streamlit/
├── app.py                       # Punto de entrada
├── requirements.txt             # Dependencia Streamlit
├── iniciar_windows.bat          # Inicio rápido en Windows (tras instalar)
├── .streamlit/
│   └── config.toml              # Colores y estilo
├── ind_app/
│   ├── config.py                 # Constantes, campos informados por IND
│   ├── styles.py                 # Estilos de interfaz
│   └── screens/
│       ├── home.py              # Primera pantalla, ya implementada
│       ├── profesor.py          # Vista de demostración
│       └── ind.py               # Vista de demostración
├── docs/
│   └── ALCANCE.md               # Qué está hecho y qué falta
└── tests/
    └── test_config.py           # Comprobación de configuración
```

## Cómo ejecutar en Windows (PowerShell)

1. Instala Python 3.10 o superior desde https://www.python.org/downloads/ , si aún no lo tienes. Activa «Add python.exe to PATH» si se ofrece.
2. Descomprime el ZIP y abre PowerShell dentro de la carpeta `IND_Preinscripciones_Streamlit`.
3. Ejecuta:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

**Si Windows bloquea la activación de scripts**, puedes evitar activarla:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

4. Abre el enlace local que aparezca en la terminal, normalmente `http://localhost:8501`.
5. Para detener el servidor, presiona `Ctrl+C` en PowerShell.

Después de instalar las dependencias, también puedes usar `iniciar_windows.bat` **si Streamlit está instalado en el Python al que apunta `py`**. Si usas entorno virtual, se recomienda iniciar con el comando correspondiente a `.venv`.

## Qué funciona hoy

- Inicio visual con el objetivo del proyecto y dos perfiles.
- Botones para entrar a demostraciones de Profesor/a e IND y volver.
- Resumen del flujo esperado: IND → Profesor/a → Validación → Excel → SIGI.
- Lista de campos comunicados por el IND.

## Qué NO funciona todavía

No se guardan ni envían inscripciones; no hay login institucional, base de datos, creación de convocatorias ni exportación SIGI. La generación del archivo Excel será una siguiente etapa cuando tengamos la plantilla oficial sin datos reales.

## Plan inmediato

1. Revisar la plantilla SIGI real (estructura, columnas, tipos y codificación).
2. Crear el formulario de preinscripción para profesores.
3. Implementar validaciones del RUT, datos y plazos.
4. Añadir almacenamiento **solo tras definir una solución adecuada de seguridad**.
5. Construir la exportación de Excel e iniciar pruebas con datos ficticios.
