"""Datos y etiquetas del prototipo basados en plantilla SIGI proporcionada por IND.

El orden de las 10 columnas está documentado, pero las reglas de validación del
importador SIGI aún necesitan una prueba autorizada con la institución.
"""

APP_TITLE = "Preinscripción Deportiva"
ORG = "IND · Dirección Regional de Aysén"

# Campos comunicados por el equipo de Deporte Competitivo del IND.
CAMPOS_INFORMADOS_SIGI = (
    "RUT",
    "Nombre",
    "Apellido paterno",
    "Apellido materno",
    "Fecha de nacimiento",
    "Género (F/M)",
    "Categoría (SUB 10-12-14-17)",
    "Disciplina",
    "Establecimiento",
    "Comuna",
)

PAGES = {"inicio", "profesor", "ind"}
