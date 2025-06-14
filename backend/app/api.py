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



@app.route("/")
def home():
    return "<h2>Welcome to our MOMO API<h2>"

@app.route('/parse-xml', methods=['POST'])
def upload_and_parse():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    filepath = os.path.join("db", file.filename)
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