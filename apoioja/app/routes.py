from flask import Blueprint, render_template, request, jsonify, current_app as app
from .models import Report, db
from .chatbot import get_gemini_response, get_fallback_response

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/denuncia")
def denuncia():
    return render_template("denuncia.html")

@bp.route("/api/submit", methods=["POST"])
def submit():
    data = request.get_json() or {}
    category = data.get("category", "").strip()
    description = data.get("description", "").strip()
    location = data.get("location", "").strip()

    if not (category and description and location):
        return jsonify({"error": "Preencha todos os campos."}), 400

    report = Report(category=category, description=description, location=location)
    db.session.add(report)
    db.session.commit()
    return jsonify({"status": "ok", "message": "Denúncia registrada com sucesso!"})

@bp.route("/api/chat", methods=["POST", "GET"])
def chat():
    if request.method == "GET":
        return jsonify({"info": "Use POST com JSON {'message': 'texto'} para conversar."})
    data = request.get_json() or {}
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"error": "Mensagem vazia."}), 400

    reply = get_gemini_response(message)
    if reply:
        return jsonify({"reply": reply})

    # fallback
    return jsonify({"reply": get_fallback_response()})
