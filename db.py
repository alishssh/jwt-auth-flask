from flask_app import create_app, db
from flask_app.models import User

app = create_app()

with app.app_context():
    users = User.query.all()
    print("✅ Users in database:", users)
