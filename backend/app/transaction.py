import xml.etree.ElementTree  as ET
import logging
import sqlite3
import os
import re
from datetime import datetime


# Logging setup
logging.basicConfig(
            filename='logs/transaction_processing.log', 
                level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s'
                    )

# Ensure necessary directories exist
os.makedirs("db", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# Connect to SQLite database
conn = sqlite3.connect('db/data.db')
cursor = conn.cursor()

# Ensure table exists
cursor.execute('''
                   CREATE TABLE IF NOT EXISTS sms_transactions (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                                       type TEXT,
                                               amount REAL,
                                                       date TEXT,
                                                               details TEXT
                                                                   )
               ''')

               def parse_sms_from_xml(file_path):
                   try:
                           tree = ET.parse(file_path)
                                   root = tree.getroot()
                                           messages = [sms.attrib.get('body', '') for sms in root.findall('sms')]
                                                   return messages
                                                       except Exception as e:
                                                               logging.error(f"Failed to parse XML: {e}")
                       return []

               def extract_transaction_info(message):
                   try:
                       amount_match = re.search(r"(\d{1,3}(?:,\d{3})*|\d+) RWF", message)
                       amount = float(amount_match.group(1).replace(",", "")) if amount_match else None

                       date_match = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", message)
                       date = date_match.group(1) if date_match else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                       return amount, date
                   except Exception as e:
                       logging.warning(f"Could not extract fields from message: {message} | Error: {e}")
                       return None, None

               def categorize_message(message):
                   lower_msg = message.lower()
                   categories = [
                               ("Incoming Money", ["received", "you have received"]),
                                       ("Payments to Code Holders", ["payment", "code holder"]),
                                               ("Transfers to Mobile Numbers", ["transfer"]),
                                                       ("Bank Deposits", ["deposit"]),
                                                               ("Airtime Bill Payments", ["airtime"]),
                                                                       ("Cash Power Bill Payments", ["cash power"]),
                                                                               ("Transactions Initiated by Third Parties", ["initiated by"]),
                                                                                       ("Withdrawals from Agents", ["withdrawal"]),
                                                                                               ("Bank Transfers", ["bank transfer"]),
                                                                                                       ("Internet and Voice Bundle Purchases", ["internet", "bundle"])
                                                                                                           ]

                   for category, keywords in categories:
                       if any(kw in lower_msg for kw in keywords):
                           return category
                           return None

                       def process_transactions(file_path):
                               messages = parse_sms_from_xml(file_path)
                                   processed_count = 0

                                       for msg in messages:
                                                   category = categorize_message(msg)
                                                           amount, date = extract_transaction_info(msg)

                                                                   if category:
                                                                                   try:
                                                                                                       cursor.execute('''
                                                                                                                                          INSERT INTO sms_transactions (type, amount, date, details)
                                                                                                                                          VALUES (?, ?, ?, ?)
                                                                                                                                      ''', (category, amount, date, msg))
                                                                                                                                      processed_count += 1
                                                                                                                                  except Exception as e:
                                                                                                                                      logging.error(f"Failed to insert transaction: {e} | Message: {msg}")
                                                                                                                              else:
                                                                                                                                  logging.info(f"Uncategorized message: {msg}")

                                                                                                                          conn.commit()
                                                                                                                              logging.info(f"Processed {processed_count} messages successfully.")

                                                                                                                      if __name__ == "__main__":
                                                                                                                          process_transactions('backend/modified_sms_v2.xml')
                                                                                                                          cursor.close()
                                                                                                                          conn.close()
                                                                                                                          print("Transaction processing completed.")
