# Casos y resultados de prueba

Los resultados oficiales se deben obtener ejecutando `python -m unittest discover -s tests -v` en el entorno del equipo. La tabla indica el resultado esperado; no debe presentarse como una captura de ejecución si aún no se ejecutó.

| ID | Tipo | Escenario | Resultado esperado |
|---|---|---|---|
| CP-01 | Unitaria | Registrar con todos los campos válidos | Redirección a detalle y código con formato `SOL-XXXXXXXXXX` |
| CP-02 | Unitaria / error | Enviar solicitante vacío | HTTP 400, mensaje de campo obligatorio y sin archivo de datos creado |
| CP-03 | Unitaria / error | Enviar categoría fuera de las opciones | HTTP 400 y mensaje de categoría inválida |
| CP-04 | Integración | Registrar, persistir en JSON y consultar por código | Detalle HTTP 200 con los datos guardados |
| CP-05 | Integración | Asignar técnico y cambiar estado | JSON actualizado e historial con ambos cambios |
| CP-06 | Aceptación | Registrar → consultar → asignar técnico → cambiar a Asignada → cambiar a Resuelta | Estado final Resuelta, técnico asignado e historial conservado |
| CP-07 | Error | Consultar código inexistente | HTTP 404 y mensaje que indica que no se encontró la solicitud |
| CP-08 | Error | Intentar asignar estado no permitido | Se mantiene el estado previo y se informa el error |

## Registro de ejecución

Completar después de ejecutar las pruebas en el equipo:

- Fecha y hora:
- Integrante que ejecutó:
- Versión/commit probado:
- Comando ejecutado: `python -m unittest discover -s tests -v`
- Pruebas aprobadas:
- Pruebas fallidas:
- Observaciones:
- Ruta de la captura o log:
