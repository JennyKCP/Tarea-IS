"""Sistema de solicitudes con persistencia local en JSON (sin base de datos)."""
from flask import Flask, render_template, request, redirect, url_for, flash
from pathlib import Path
from datetime import datetime, timezone
from threading import RLock
import json
import os
import uuid

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = Path(os.environ.get("SOLICITUDES_DATA_FILE", BASE_DIR / "data" / "solicitudes.json"))
LOCK = RLock()
CATEGORIAS = {"Soporte técnico", "Software", "Hardware", "Redes", "Otro"}
PRIORIDADES = {"Baja", "Media", "Alta", "Crítica"}
ESTADOS = {"Registrada", "Asignada", "En proceso", "Resuelta", "Cerrada"}


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(SECRET_KEY=os.environ.get("FLASK_SECRET_KEY", "dev-only-change-me"), TESTING=False)
    if test_config:
        app.config.update(test_config)

    def data_path():
        return Path(app.config.get("DATA_FILE", DATA_FILE))

    def load_all():
        path = data_path()
        if not path.exists():
            return {}
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, dict) else {}
        except (json.JSONDecodeError, OSError):
            raise RuntimeError("No se pudo leer el archivo de solicitudes. Verifique que el JSON sea válido.")

    def save_all(data):
        path = data_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = path.with_suffix(path.suffix + ".tmp")
        with temp_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        temp_path.replace(path)

    def now():
        return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")

    def clean(value):
        return value.strip() if isinstance(value, str) else ""

    def validate_form(form):
        fields = {
            "solicitante": clean(form.get("solicitante")),
            "categoria": clean(form.get("categoria")),
            "descripcion": clean(form.get("descripcion")),
            "prioridad": clean(form.get("prioridad")),
        }
        errors = []
        labels = {"solicitante": "El nombre del solicitante", "categoria": "La categoría", "descripcion": "La descripción", "prioridad": "La prioridad"}
        for key, value in fields.items():
            if not value:
                errors.append(f"{labels[key]} es obligatorio.")
        if fields["categoria"] and fields["categoria"] not in CATEGORIAS:
            errors.append("Seleccione una categoría válida.")
        if fields["prioridad"] and fields["prioridad"] not in PRIORIDADES:
            errors.append("Seleccione una prioridad válida.")
        if len(fields["solicitante"]) > 100:
            errors.append("El nombre del solicitante no debe superar 100 caracteres.")
        if len(fields["descripcion"]) > 2000:
            errors.append("La descripción no debe superar 2000 caracteres.")
        return fields, errors

    @app.get("/")
    def index():
        with LOCK:
            solicitudes = sorted(load_all().values(), key=lambda s: s["creada_en"], reverse=True)
        return render_template("index.html", solicitudes=solicitudes, categorias=sorted(CATEGORIAS), prioridades=["Baja", "Media", "Alta", "Crítica"])

    @app.post("/solicitudes")
    def registrar():
        fields, errors = validate_form(request.form)
        if errors:
            for error in errors:
                flash(error, "error")
            return render_template("index.html", solicitudes=sorted(load_all().values(), key=lambda s: s["creada_en"], reverse=True), categorias=sorted(CATEGORIAS), prioridades=["Baja", "Media", "Alta", "Crítica"], form_data=fields), 400
        codigo = "SOL-" + uuid.uuid4().hex[:10].upper()
        timestamp = now()
        solicitud = {
            "codigo": codigo, **fields, "tecnico": "", "estado": "Registrada",
            "creada_en": timestamp,
            "historial": [{"fecha": timestamp, "campo": "estado", "valor_anterior": "", "valor_nuevo": "Registrada", "detalle": "Solicitud registrada"}]
        }
        with LOCK:
            data = load_all()
            while codigo in data:
                codigo = "SOL-" + uuid.uuid4().hex[:10].upper()
                solicitud["codigo"] = codigo
            data[codigo] = solicitud
            save_all(data)
        flash(f"Solicitud registrada correctamente. Código: {codigo}", "success")
        return redirect(url_for("detalle", codigo=codigo))

    @app.get("/solicitudes/<codigo>")
    def detalle(codigo):
        with LOCK:
            solicitud = load_all().get(clean(codigo).upper())
        if not solicitud:
            return render_template("no_encontrada.html", codigo=codigo), 404
        return render_template("detalle.html", solicitud=solicitud, estados=["Asignada", "En proceso", "Resuelta", "Cerrada"])

    @app.post("/solicitudes/<codigo>/actualizar")
    def actualizar(codigo):
        codigo = clean(codigo).upper()
        tecnico = clean(request.form.get("tecnico"))
        estado = clean(request.form.get("estado"))
        if len(tecnico) > 100:
            flash("El nombre del técnico no debe superar 100 caracteres.", "error")
            return redirect(url_for("detalle", codigo=codigo))
        if estado and estado not in ESTADOS:
            flash("Seleccione un estado válido.", "error")
            return redirect(url_for("detalle", codigo=codigo))
        if not tecnico and not estado:
            flash("Indique un técnico, un estado o ambos para actualizar la solicitud.", "error")
            return redirect(url_for("detalle", codigo=codigo))
        with LOCK:
            data = load_all()
            solicitud = data.get(codigo)
            if not solicitud:
                return render_template("no_encontrada.html", codigo=codigo), 404
            timestamp = now()
            if tecnico and tecnico != solicitud["tecnico"]:
                solicitud["historial"].append({"fecha": timestamp, "campo": "tecnico", "valor_anterior": solicitud["tecnico"], "valor_nuevo": tecnico, "detalle": "Asignación/actualización de técnico"})
                solicitud["tecnico"] = tecnico
            if estado and estado != solicitud["estado"]:
                anterior = solicitud["estado"]
                solicitud["estado"] = estado
                solicitud["historial"].append({"fecha": timestamp, "campo": "estado", "valor_anterior": anterior, "valor_nuevo": estado, "detalle": "Cambio de estado"})
            save_all(data)
        flash("Solicitud actualizada correctamente.", "success")
        return redirect(url_for("detalle", codigo=codigo))

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("no_encontrada.html", codigo="recurso"), 404

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG", "0") == "1")
