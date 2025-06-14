from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class UserModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(80),unique=True,nullalbe=False)
    email = db.Column(db.String(80),unique=True,nullalbe=False)

    def __repr__(self):
        return f"User(name = {self.user_namename}, email = {self.email})"

@app.route("/")
def home():
    return "<h2>Welcome to our MOMO API<h2>"

if __name__ == "__main__":
    app.run(debug=True)