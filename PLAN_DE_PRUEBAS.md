# Pruebas para presentar el avance al IND

**Regla esencial:** utilizar solo inscripciones completamente ficticias; nunca registrar antecedentes reales de estudiantes. La validación del Excel en SIGI se debe efectuar únicamente si el IND autoriza un entorno y procedimiento de prueba.

| ID | Prueba | Acción | Resultado esperado |
|---|---|---|---|
| P01 | Acceso por roles | Iniciar sesión como profesor e intentar ingresar al panel IND | No se muestra el panel ni sus datos. |
| P02 | Convocatoria | Entrar como IND y publicar una convocatoria de prueba | Profesor la ve desde su navegador. |
| P03 | Persistencia | Profesor envía datos ficticios; IND consulta desde otro dispositivo | Registro visible en el panel IND. |
| P04 | RUT inválido | Profesor ingresa un RUT de prueba con DV incorrecto | Se rechaza desde el formulario. |
| P05 | Plazo cerrado | IND despublica convocatoria o configura fecha cerrada | El profesor no puede enviar un registro. La regla también existe en la base de datos. |
| P06 | Duplicidad | Profesor intenta enviar el mismo RUT + disciplina en la misma convocatoria | La base de datos impide el segundo registro. |
| P07 | Privacidad por usuario | Otro profesor inicia sesión y consulta registros | No puede ver registros creados por otros profesores. |
| P08 | Validación IND | IND marca un registro como validado | El registro cambia de estado. |
| P09 | Excel | IND descarga el archivo de registros validados | Se conservan las hojas `datos` y `Options`, los dos encabezados y el orden de las 10 columnas. |
| P10 | Cupos orientativos | Recibir más solicitudes que las planificadas | Panel muestra advertencia, sin bloquear automáticamente inscripciones. |

**Evidencias sugeridas para la presentación final:** capturas de ambas interfaces, resultados de P01–P10, diagrama AS-IS/TO-BE, plantilla de salida, validación por el IND y comparación de tiempos medidos (cuando esté disponible).
