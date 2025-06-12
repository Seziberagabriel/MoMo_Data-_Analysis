import xml.etree.ElementTree as ET
import logging


# Logging setup
logging.basicConfig(filename='unprocessed_messages.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    sms_data = []
    for sms in root.findall('sms'):
        body = sms.find('body').text
        sms_data.append(body)

    return sms_data

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
    
    for message in sms_data;
        # will populate the categorize_data dictionary
        # with the appropriate message category