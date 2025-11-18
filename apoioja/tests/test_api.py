import json
from app import create_app, db
from app.models import Report

#se der erro, substitua acima pelo código abaixo:
#import sys, os
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
#from app import create_app, db

def setup_app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
    return app

def test_index():
    app = setup_app()
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200

def test_submit_success():
    app = setup_app()
    client = app.test_client()
    payload = {"category":"teste","description":"desc","location":"local"}
    resp = client.post("/api/submit", json=payload)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "ok"

def test_submit_missing():
    app = setup_app()
    client = app.test_client()
    resp = client.post("/api/submit", json={})
    assert resp.status_code == 400
