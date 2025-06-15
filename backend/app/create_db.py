from api import app, db
from models import UserModel,sms_transactions

with app.app_context():
    db.create_all()
