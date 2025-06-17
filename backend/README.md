# MTN MoMo SMS Dashboard API

This project is a Flask-based backend service that parses MTN Mobile Money SMS messages in XML format, categorizes and stores them in a local SQLite database, and exposes a set of API endpoints to interact with the data. It also includes a utility for exporting the database contents to JSON.

---

## 🧠 Features

- ✅ XML file upload and parsing
- ✅ Categorization of SMS into meaningful transaction types
- ✅ SQLite database storage (`db/data.db`)
- ✅ JSON export utility
- ✅ RESTful API built with Flask
- ✅ Error logging and unprocessed message tracking

---

## 📁 Project Structure

- `app/`
	+ `api.py`: RESTful API endpoints
	+ `config.py`: database configuration
	+ `models.py`: database models
	+ `parser_xml.py`: XML parser utility
	+ `transaction_model.py`: transaction model
- `db/`: database files
	+ `data.db`: SQLite database file
- `exports/`: JSON export utility
	+ `export_to_json.py`: JSON export script
- `logs/`: error log files
	+ `unprocessed_messages.log`: log of unprocessed messages
- `requirements.txt`: Python package dependencies
- `README.md`: this file


---

## 🚀 Getting Started

### 🧱 Prerequisites

- Python 3.8+
- pip (Python package manager)

### 🔧 Installation

1. **Clone the Repository**

```bash
# git clone https://github.com/Seziberagabriel/MoMo_Data-_Analysis.git
# cd momo-sms-dashboard/backend


# 2. Create a virtual environment (recommended)
# python3 -m venv .venv
# source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate

# 3. Install dependencies
# pip install flask


# 🛠️ Running the Backend Server
# From the backend/ folder
# python api.py
# By default, the server runs on http://127.0.0.1:5000.



🌐 Available API Endpoints
# POST /parse-xml
# Upload XML file and parse messages

# Form-data Key: file
# Response:
# { "message": "File parsed and data stored successfully." }


## GET /get-raw-data
# Returns all transaction entries as readable strings.
# Response:
[
  "Type: Incoming Money, Amount: 2000, Date: 2024-01-01 10:00:00, Details: You have received 2000 RWF from..."
]


# 📤 Exporting Data to JSON
# To convert all stored transactions to a JSON file:

# python export_to_json.py
# Output will be stored as:
# db/sms_data.json


🗃️ Database Schema
#  Table: sms_transactions


# | id  | type                     | amount | date                | details              |
# | --- | ------------------------ | ------ | ------------------- | -------------------- |
# | 1   | Incoming Money           | 5000   | 2024-01-01 10:00:00 | You have received... |
# | 2   | Payments to Code Holders | 1000   | 2024-01-02 14:30:00 | Your payment of...   |
# | ... | ...                      | ...    | ...                 | ...                  |
