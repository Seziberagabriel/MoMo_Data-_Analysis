import xml.etree.ElementTree as ET
import sqlite3
import logging
import os
import re
from datetime import datetime


# Set up logging
logging.basicConfig(filename='unprocessed_messages.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Ensure the db directory exists
os.makedirs("db", exist_ok=True)

# SQLite DB setup
conn = sqlite3.connect('db/data.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS sms_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    amount INTEGER,
    date TEXT,
    details TEXT
)
''')

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    sms_data = []

    for sms in root.findall('sms'):
        body_element = sms.get('body')
        if body_element is not None:
            sms_data.append(body_element)
        else:
            logging.info('Missing body attribute in SMS entry.')

    return sms_data

def extract_fields(message):
    try:
        amount_match = re.search(r"(\d{1,3}(?:,\d{3})*|\d+) RWF", message)
        amount = int(amount_match.group(1).replace(",", "")) if amount_match else None

        date_match = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", message)
        date = date_match.group(1) if date_match else None

        return amount, date
    except Exception as e:
        logging.info(f"Failed to extract fields: {message} - Error: {e}")
        return None, None

def categorize_sms(sms_data):
    for message in sms_data:
        amount, date = extract_fields(message)
        category = None

        if "received" in message.lower():
            category = 'Incoming Money'
        elif "payment" in message.lower():
            category = 'Payments to Code Holders'
        elif "transfer" in message.lower():
            category = 'Transfers to Mobile Numbers'
        elif "deposit" in message.lower():
            category = 'Bank Deposits'
        elif "airtime" in message.lower():
            category = 'Airtime Bill Payments'
        elif "cash power" in message.lower():
            category = 'Cash Power Bill Payments'
        elif "withdrawal" in message.lower():
            category = 'Withdrawals from Agents'
        elif "bank transfer" in message.lower():
            category = 'Bank Transfers'
        elif "internet" in message.lower() or "bundle" in message.lower():
            category = 'Internet and Voice Bundle Purchases'
        else:
            category = 'Uncategorized'

        if category != 'Uncategorized' and amount is not None:
            try:
                cursor.execute('''
                    INSERT INTO sms_transactions (type, amount, date, details)
                    VALUES (?, ?, ?, ?)
                ''', (category, amount, date, message))
            except Exception as e:
                logging.info(f"Insert failed: {message} - Error: {e}")
        else:
            logging.info(f'Unprocessed or invalid message: {message}')

if __name__ == "__main__":
    file_path = './backend/modified_sms_v2.xml'  # Update with the actual path
    sms_data = parse_xml(file_path)
    categorize_sms(sms_data)
    conn.commit()
    cursor.close()
    conn.close()
    print("Categorized and stored SMS data in db/data.db")

    # Test the SQLite database
    conn = sqlite3.connect('db/data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM sms_transactions')
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    cursor.close()
    conn.close()