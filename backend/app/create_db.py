from api import app, db
from models import UserModel

with app.app_context():
    db.create_all()
