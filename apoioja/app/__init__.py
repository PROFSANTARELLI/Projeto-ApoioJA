from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()  # carrega .env se existir

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///apoioja.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "trocar_em_producao")

    db.init_app(app)

    # registrar blueprints
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    # criar tabelas se não existirem
    with app.app_context():
        db.create_all()

    return app
