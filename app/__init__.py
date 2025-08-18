from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
import os
from werkzeug.utils import secure_filename
import bleach
import markdown

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'main.login'  # Updated to use blueprint prefix

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes import bp as main_bp  # Import the blueprint
    app.register_blueprint(main_bp)  # Register the blueprint

    # Debug: Print registered routes
    with app.app_context():
        print("Registered routes:", [rule.rule for rule in app.url_map.iter_rules()])

    return app