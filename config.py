"""Datos y etiquetas del prototipo inicial.

ATENCIÓN: El orden exacto, los formatos y las reglas de la plantilla
real de SIGI deben validarse antes de producir el archivo de importación.
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
    "Disciplina",
    "Establecimiento",
    "Comuna",
)

PAGES = {"inicio", "profesor", "ind"}
