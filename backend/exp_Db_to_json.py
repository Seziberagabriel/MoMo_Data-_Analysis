import sqlite3
import json
import os

# Path to database
db_file = 'db/data.db'

# Check if the database file exists
if not os.path.exists(db_file):
    print("The database file was not found.")
else:
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()

        # Fetch all rows from the table
        cursor.execute("SELECT id, type, amount, date, details FROM sms_transactions")
        rows = cursor.fetchall()

        # Define the column names manually
        column_names = ["id", "type", "amount", "date", "details"]

        # Convert the rows into a list of dictionaries
        result = []
        for row in rows:
            record = dict(zip(column_names, row))
            result.append(record)

        # Write the list to a JSON file
        with open("db/sms_data.json", "w") as json_file:
            json.dump(result, json_file, indent=4)

        print("Data was exported to db/sms_data.json successfully!")

        # Close database connection
        cursor.close()
        connection.close()

    except Exception as e:
        print("Something went wrong:", e)

    finally:
        if connection:
            connection.close()
