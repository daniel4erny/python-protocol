import sqlite3, os
from colorama import Fore, Style, init

init(autoreset=True)

def openDb():
    try:
        global coolDB, cursor
        db_path = os.path.join(os.path.dirname(__file__), "coolDB.db")
        coolDB = sqlite3.connect(db_path)
        cursor = coolDB.cursor()
        print(Fore.LIGHTYELLOW_EX + "[✓] db initiated")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            vek INTEGER
        )
        """)
        print(Fore.LIGHTYELLOW_EX + "[✓] table messages initiated")
        coolDB.commit()
    except Exception as e:
        print(Fore.RED + "[x] an error ocurred while initiating the database")
        print(Fore.RED + f"{e}")

def writeMsg():
    return 0
