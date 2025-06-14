# config.py
import sqlite3
import os

def get_connection():
    os.makedirs("db", exist_ok=True)
    return sqlite3.connect("db/new_postman_test.db")
