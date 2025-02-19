from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_app.config import Config
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    bcrypt.init_app(app)
    db.init_app(app)
    Migrate(app, db)
    jwt.init_app(app)
    login_manager.init_app(app)

    with app.app_context():  # Ensure the app context is used correctly
        db.create_all()

    from flask_app.routes import auth_bp, product_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)

    return app
