import sqlite3
from dotenv import load_dotenv
import os
import colorama

BARVICKA = colorama.Fore.LIGHTYELLOW_EX
RED = colorama.Fore.RED

load_dotenv()
db_path = os.getenv("DATABASE_PATH")
print(db_path)

def openDB():
    try:
        coolDB = sqlite3.connect(db_path)
        print(BARVICKA + "DB WORKS EZ PZ")
        cursor = coolDB.cursor()
        cursor.execute("""
CREATE TABLE IF NOT EXISTS zpravicky(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    zpravy TEXT,
    date DATETIME DEFAULT CURRENT_TIMESTAMP      
    )""")
        return cursor
    except Exception as e:
        print(RED + e)

def zapsatZpravu(zprava, cursor):
    try:
        cursor.execute("""
INSERT INTO """)