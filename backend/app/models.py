from api import db




class UserModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(80),unique=True,nullable=False)
    email = db.Column(db.String(80),unique=True,nullable=False)

    def __repr__(self):
        return f"User(name = {self.user_namename}, email = {self.email})"