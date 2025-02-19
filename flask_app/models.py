from flask_login import UserMixin
from flask_app import db
import bcrypt

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)  # Store hashed passwords
    role = db.Column(db.String(10), nullable=False)  

    def set_password(self, password):
        """Hashes the password before storing it."""
        self.hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        """Verifies the password against the stored hash."""
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password.encode('utf-8'))

    def __repr__(self):
        return f"<User {self.username}>"

from flask_app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ✅ Ensures auto-increment
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

