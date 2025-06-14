from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)



@app.route("/")
def home():
    return "<h2>Welcome to our MOMO API<h2>"

if __name__ == "__main__":
    app.run(debug=True)