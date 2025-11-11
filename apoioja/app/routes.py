from flask import render_template, request, jsonify
from app import app, db
from app.models import Report

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/denuncia')
def denuncia():
    return render_template('denuncia.html')

@app.route('/api/reports', methods=['POST'])
def create_report():
    data = request.get_json()
    new_report = Report(
        category=data.get('category'),
        description=data.get('description'),
        location=data.get('location')
    )
    db.session.add(new_report)
    db.session.commit()
    return jsonify({"message": "Denúncia registrada com sucesso!"}), 201
