import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def load_env_file(env_path):
    """Simple, zero-dependency .env loader."""
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                key, val = line.split('=', 1)
                key = key.strip()
                val = val.strip().strip("'\"")
                if key and key not in os.environ:
                    os.environ[key] = val


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Configure paths and load environment variables from .env
    basedir = os.path.abspath(os.path.dirname(__file__))
    env_file = os.path.join(basedir, "../.env")
    load_env_file(env_file)

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["GM_PASSWORD_HASH"] = os.environ.get("GM_PASSWORD_HASH")
    app.config["PLAYER_PASSWORD_HASH"] = os.environ.get("PLAYER_PASSWORD_HASH")

    # Configure database path
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "../instance/local.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register Blueprints
    from project.auth import auth_bp
    app.register_blueprint(auth_bp)

    from project.main.routes import main_bp
    app.register_blueprint(main_bp)

    # Global context processor for auth state
    from project.auth.utils import get_current_role, is_authenticated

    @app.context_processor
    def inject_auth():
        return {
            'current_role': get_current_role(),
            'is_authenticated': is_authenticated(),
        }

    # Import models so Alembic detects them automatically
    with app.app_context():
        from project.main import models

    return app
