import xml.etree.ElementTree as ET
import sqlite3
import re
from datetime import datetime

DB_NAME = 'sms_transactions.db'
LOG_FILE = 'unprocessed_sms.log'

# Define categories
CATEGORIES = {
    "incoming_money": ["received", "credited"],
    "payment_code": ["payment code"],
    "transfer_mobile": ["sent to", "transferred to"],
    "bank_deposit": ["bank deposit", "credited to your bank"],
    "airtime_payment": ["airtime", "recharge"],
    "cash_power": ["cash power", "electricity"],
    "third_party": ["initiated by"],
    "withdrawal_agent": ["agent withdrawal"],
    "bank_transfer": ["bank transfer"],
    "bundle_purchase": ["bundle", "internet", "voice"]
}

def categorize_sms(message):
    msg_lower = message.lower()
    for category, keywords in CATEGORIES.items():
        if any(keyword in msg_lower for keyword in keywords):
            return category
    return "unknown"

def normalize_amount(amount_str):
    match = re.search(r'(\d+[.,]?\d*)', amount_str.replace(",", ""))
    if match:
        return float(match.group(1))
    return None

def normalize_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except:
        return None

def log_unprocessed(message):
    with open(LOG_FILE, 'a') as f:
        f.write(message + "\n")

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        sender TEXT,
        receiver TEXT,
        amount REAL,
        category TEXT,
        original_message TEXT
    )
    """)
    conn.commit()
    conn.close()

def insert_transaction(data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO transactions (date, sender, receiver, amount, category, original_message)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data.get("date"),
        data.get("sender"),
        data.get("receiver"),
        data.get("amount"),
        data.get("category"),
        data.get("original_message")
    ))
    conn.commit()
    conn.close()

def process_sms_file(xml_path):
    create_tables()
    tree = ET.parse(xml_path)
    root = tree.getroot()

    for sms in root.findall('sms'):
        try:
            message = sms.get('body')
            if not message:
                log_unprocessed("No message body")
                continue

            category = categorize_sms(message)
            amount = normalize_amount(message)
            date = normalize_date(sms.get('date', ''))

            if not amount or not date:
                log_unprocessed(message)
                continue

            data = {
                "date": date.strftime("%Y-%m-%d %H:%M:%S"),
                "sender": sms.get('address'),
                "receiver": "MTN",  # Assuming messages come from MTN
                "amount": amount,
                "category": category,
                "original_message": message
            }

            insert_transaction(data)

        except Exception as e:
            log_unprocessed(f"Error processing message: {message} | Error: {str(e)}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python user.py path_to_sms.xml")
    else:
        process_sms_file(sys.argv[1])

