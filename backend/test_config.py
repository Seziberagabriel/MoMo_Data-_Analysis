# config.py
import sqlite3
import os


def get_connection():
    os.makedirs("db", exist_ok=True)
<<<<<<< HEAD
    return sqlite3.connect("db/test2_data.db")
=======
    return sqlite3.connect("db/new_postman_test.db")
>>>>>>> b133ca3357bee1f0dea5ffa00ce5ad053087361a
