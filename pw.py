from flask_app import app, db, bcrypt
from flask_app.models import User

with app.app_context():
    user = User.query.filter(User.username.ilike("alish")).first()  # Case-insensitive search
    if user:
        new_password = "Alish@123"
        user.hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        db.session.commit()
        print(f"Password reset successfully for user: {user.username}")
    else:
        print("User not found.")
