import xml.etree.ElementTree as ET
import logging
from datetime import datetime
import sqlite3
import os
import re


# Logging setup
logging.basicConfig(filename='unprocessed_messages.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# making sure db directory exists
os.makedirs("db", exist_ok=True)

# sqlite database setup
conn = sqlite3.connect('db/data.db')
cursor = conn.cursor()


# SQLite table creation if one doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sms_transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        amount REAL,
        date TEXT,
        details TEXT
    )
''')

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    sms_data = []
    
    for sms in root.findall('sms'):
        body_element = sms.find('body')
        if body_element is not None:
            body = body_element.text
            sms_data.append(body)
        else:
            logging.info(f"Missing body element in SMS")
        
    return sms_data

def extract_fields(message):
    try:
        amount_match = re.search(r"(\d{1,3}(?:,\d{3})*|\d+) RWF", message)
        amount = int(amount_match.group(1).replace(",", "")) if amount_match else None

        txid_match = re.search(r"TxId[:* ]*(\d+)|Transaction ID[: ]*(\d+)|Financial Transaction Id[: ]*(\d+)", message)
        txid = txid_match.group(1) or txid_match.group(2) or txid_match.group(3) if txid_match else None

        date_match = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", message)
        date = date_match.group(1) if date_match else None

        return amount, date, txid
    except Exception as e:
        logging.info(f"Failed to extract fields: {message} - Error: {e}")
        return None, None, None

def categorize_sms(sms_data):
    categorize_data = {
        'Incoming Money' : [],
        'Payments to Code Holders' : [],
        'Transfers to Mobile Numbers' : [],
        'Bank Deposits' : [],
        'Airtime Bill Payments' : [],
        'Cash Power Bill Payments' : [],
        'Transactions Initiated by Third Parties' : [],
        'Withdrawals from Agents' : [],
        'Bank Transfers' : [],
        'Internet and Voice Bundle Purchases' : [],
    }
    
    for message in sms_data:
        amount, date, txid = extract_fields(message)
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
            
        if category:
            categorize_data[category].append(message)
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO sms_transactions (type, amount, date, details)
                    VALUES (?, ?, ?, ?)
                ''', (category, message, amount, date, txid))
            except Exception as e:
                logging.info(f"Insert failed: {message} - Error: {e}")
        else:
            logging.info(f'Unprocessed message: {message}')

    return categorize_data

if __name__ == "__main__":
    file_path = './backend/modified_sms_v2.xml'  # Update with the actual path
    sms_data = parse_xml(file_path)
    categorized_data = categorize_sms(sms_data)
    conn.commit()
    cursor.close()
    conn.close()
    print("Extraction, cleaning, categorization, and SQLite insertion complete.")
