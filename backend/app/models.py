from api import db




class UserModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(80),unique=True,nullable=False)
    email = db.Column(db.String(80),unique=True,nullable=False)

    def __repr__(self):
        return f"User(name = {self.user_namename}, email = {self.email})"
    

class sms_Transaction(db.Midel):
    id = db.Column(db.Integer,primary_key=True)
    type = db.Column(db.String(80))
    amount = db.Column(db.Integer)
    date = db.Column(db.String(80))
    details = db.Column(db.String(80))
    
    def __repr__(self):
        return f"Transaction(type = {self.type}, Amount = {self.amount}, Date = {self.date}, Deteils = {self.details} )"
   
