import sqlite3, os
from colorama import Fore, Style, init
import hashlib

init(autoreset=True)

def openDb():
    try:
        global coolDB, cursor
        db_path = os.path.join(os.path.dirname(__file__), "coolDB.db")
        coolDB = sqlite3.connect(db_path)
        cursor = coolDB.cursor()
        print(Fore.LIGHTYELLOW_EX + "[✓] db initiated")
        print(Fore.CYAN + f"[i] Database path: {db_path}")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            text TEXT,
            password TEXT,
            date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)

        print(Fore.LIGHTYELLOW_EX + "[✓] table messages initiated")
        coolDB.commit()
    except Exception as e:
        print(Fore.RED + "[x] an error ocurred while initiating the database")
        print(Fore.RED + f"{e}")

def writeMsg(userName, messageText, passwordText):
    try:
        passwordText = hashlib.md5(passwordText).hexdigest()
        cursor.execute("""
            INSERT INTO messages (user, text, password) 
            VALUES (?, ?, ?)
            """, (userName, messageText, passwordText))
        coolDB.commit()
        print(Fore.LIGHTYELLOW_EX + f"[✓] zpráva uložena do DB s id {cursor.lastrowid}")
    except Exception as e:
        print(Fore.RED + f"[x] and error occured while saving the message {e}")

def getMsg(notHashedPassword):
    try:
        notHashedPassword = notHashedPassword.md
        cursor.execute("""SELECT * FROM messages WHERE id = ?""", (notHashedPassword,))
        print(Fore.LIGHTYELLOW_EX + "[✓] db fetching message")
        return cursor.fetchall()
    except Exception as e:
        print(Fore.RED + f"[x] and error occured while fetching the message {e}")