from api import app, db,UserModel,sms_transactions

with app.app_context():
    db.create_all()
