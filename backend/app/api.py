from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_restful import Resource, Api, reqparse, fields , marshal_with, abort
import os
from parser_xml import parse, categorize_sms
import logging



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)

class UserModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(80),unique=True,nullable=False)
    email = db.Column(db.String(80),unique=True,nullable=False)

    def __repr__(self):
        return f"User(name = {self.user_name}, email = {self.email})"


class sms_transactions(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    type = db.Column(db.String(80))
    amount = db.Column(db.Integer)
    date = db.Column(db.String(80))
    details = db.Column(db.String(80))

    def __repr__(self):
        return f"Transaction(type = {self.type}, Amount = {self.amount}, Date = {self.date}, Details = {self.details} )"


user_args = reqparse.RequestParser()
user_args.add_argument('user_name', type=str, required=True,help="Name cannot be blank")
user_args.add_argument('email', type=str, required=True,help="Email cannot be blank")

userFields = {
    'id': fields.Integer,
    'user_name': fields.String,
    'email': fields.String,
}

class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all()
        return users
api.add_resource(Users, '/api/users/')


sms_transactions_args = reqparse.RequestParser()
sms_transactions_args.add_argument('type', type=str, required=True,help="Transaction type cannot be blank")
sms_transactions_args.add_argument('amount', type=int, required=True,help="Transaction amount cannot be blank")
sms_transactions_args.add_argument('date', type=str, required=True,help="Transaction Date cannot be blank")
sms_transactions_args.add_argument('details', type=str, required=True,help="Transaction Details cannot be blank")

sms_transactionsFields = {
    'id': fields.Integer,
    'type': fields.String,
    'amount': fields.Integer,
    'date': fields.String,
    'details': fields.String,
}

class Sms_Transactions(Resource):
    @marshal_with(sms_transactionsFields)
    def get(self):
        transactions = sms_transactions.query.all()
        return transactions
api.add_resource(Sms_Transactions, '/api/transactions/')

@app.route("/")
def home():
    return "<h2>Welcome to our MOMO API<h2>"

@app.route('/parse-xml', methods=['POST'])
def upload_and_parse():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    filepath = os.path.join("imports", file.filename)
    file.save(filepath)

    try:
        sms_data = parse(filepath)
        # print(sms_data)
        categorize_sms(sms_data)
        return jsonify({'message': 'File parsed and data stored successfully.'})
    except Exception as e:
        logging.error(f"Error parsing file: {e}")
        return jsonify({'error': 'Failed to process the file'}), 500


if __name__ == "__main__":
    app.run(debug=True)