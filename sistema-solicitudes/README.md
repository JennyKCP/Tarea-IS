# Tarea-IS
# Sistema de Solicitudes

Este proyecto fue desarrollado con Python y Flask. Permite registrar y administrar solicitudes sin usar una base de datos, ya que la información se guarda en un archivo JSON.

## Requisitos
- Python 3.10 o superior
- Git

## Instalación y ejecución

1. Abrir la carpeta del proyecto en VS Code.
2. Abrir la terminal y ejecutar:

```bash
python -m venv .venv
```

3. Activar el entorno virtual en Windows:

```bash
.venv\Scripts\activate
```

4. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

5. Ejecutar el sistema:

```bash
python app.py
```

6. Abrir en el navegador: http://127.0.0.1:5000

## Funcionalidades

- Registrar solicitudes con nombre, categoría, descripción y prioridad.
- Generar un código único para cada solicitud.
- Consultar solicitudes usando su código.
- Asignar técnicos.
- Cambiar el estado de las solicitudes.
- Guardar un historial de los cambios realizados.
- Validar los datos ingresados y mostrar mensajes de error.

## Pruebas

Para ejecutar las pruebas, usar el siguiente comando:

```bash
python -m unittest discover -s tests -v
```

Se realizan pruebas para verificar el registro, las consultas, las validaciones y el funcionamiento general del sistema.

## Uso de Git

El proyecto se administra con Git y GitHub. Se trabaja con ramas para realizar cambios y se revisan mediante Pull Requests antes de integrarlos a la rama principal `main`.

Los commits deben tener mensajes claros que indiquen los cambios realizados.

## Limitaciones

El sistema guarda los datos en un archivo JSON, por lo que está pensado para uso local y académico. No cuenta con una base de datos ni con un sistema completo de usuarios y permisos.