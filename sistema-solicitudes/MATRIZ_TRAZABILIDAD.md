# Matriz de trazabilidad

| ID | Requisito | Implementación | Prueba / evidencia | Estado |
|---|---|---|---|---|
| RF-01 | Registrar solicitante, categoría, descripción y prioridad | `app.py` → `registrar`; `templates/index.html` | `test_registro_persistencia_y_consulta` | Implementado |
| RF-02 | Generar código único | UUID en `app.py` → `registrar` | `test_registro_genera_codigo_unico` | Implementado |
| RF-03 | Consultar por código | `app.py` → `detalle` | `test_registro_persistencia_y_consulta` | Implementado |
| RF-04 | Asignar técnico | `app.py` → `actualizar` | `test_actualizacion_guarda_historial` | Implementado |
| RF-05 | Actualizar estado | `app.py` → `actualizar` | `test_actualizacion_guarda_historial`; `test_flujo_completo_aceptacion` | Implementado |
| RF-06 | Conservar historial de cambios | Campo `historial` del JSON | `test_actualizacion_guarda_historial`; `test_flujo_completo_aceptacion` | Implementado |
| RF-07 | Validar campos obligatorios | `validate_form` en `app.py`; atributos `required` en formulario | `test_rechaza_datos_incompletos` | Implementado |
| RF-08 | Mensajes comprensibles ante errores | `flash`, `no_encontrada.html`, validaciones | `test_rechaza_categoria_no_permitida`; `test_consulta_codigo_inexistente`; `test_rechaza_estado_invalido` | Implementado |
| RP-01 | Repositorio de control de versiones | Procedimiento Git del README | `git log --oneline --all` después de crear commits reales | Pendiente de ejecutar por el equipo |
| RP-02 | Rama principal protegida | Configuración de reglas en GitHub | Captura de Rulesets/Branch protection | Pendiente de configurar |
| RP-03 | Ramas de funcionalidad | Convención de nombres en README | `git branch -a` | Pendiente de ejecutar por el equipo |
| RP-04 | Cinco commits significativos mínimo | Plan de commits en README | `git log --oneline --graph --all` | Pendiente de ejecutar por el equipo |
| RP-05 | Mensajes descriptivos | Convención Conventional Commits sugerida | Historial real de Git | Pendiente de ejecutar por el equipo |
| RP-06 | Revisión por otro integrante | Pull Request obligatorio | PR aprobado por persona distinta del autor | Pendiente de ejecutar por el equipo |
| RP-07 | README con instrucciones | `README.md` | Revisión documental y ejecución local | Implementado |
| RP-08 | Sin credenciales en código | Variables de entorno y `.gitignore` | Inspección del repositorio antes del push | Implementado; revisar antes de publicar |
| PT-01 | Tres pruebas unitarias | `tests/test_solicitudes.py` | Tres métodos unitarios documentados | Implementado |
| PT-02 | Dos pruebas de integración | `tests/test_solicitudes.py` | Persistencia/consulta y actualización/historial | Implementado |
| PT-03 | Prueba de aceptación del flujo completo | `test_flujo_completo_aceptacion` | Registro → consulta → asignación → resolución | Implementado |
| PT-04 | Error por datos incompletos | `test_rechaza_datos_incompletos` | Espera HTTP 400 y mensaje de validación | Implementado |
| PT-05 | Consulta con código inexistente | `test_consulta_codigo_inexistente` | Espera HTTP 404 y mensaje comprensible | Implementado |
