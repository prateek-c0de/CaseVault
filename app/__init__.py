from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import os

db = SQLAlchemy()
csrf = CSRFProtect()

def create_app(config_class='app.config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)

    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], '..', 'app', 'static', 'qr'), exist_ok=True)

    # Register blueprints (to be created)
    from app.routes.auth import auth_bp
    from app.routes.evidence import evidence_bp
    from app.routes.custody import custody_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.verification import verification_bp
    from app.routes.audit import audit_bp
    from app.routes.cases import cases_bp
    from app.routes.documents import documents_bp
    from app.routes.search import search_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(evidence_bp, url_prefix='/evidence')
    app.register_blueprint(custody_bp, url_prefix='/custody')
    app.register_blueprint(dashboard_bp, url_prefix='/')
    app.register_blueprint(verification_bp, url_prefix='/verification')
    app.register_blueprint(audit_bp, url_prefix='/audit')
    app.register_blueprint(cases_bp, url_prefix='/cases')
    app.register_blueprint(documents_bp, url_prefix='/documents')
    app.register_blueprint(search_bp, url_prefix='/search')

    return app

