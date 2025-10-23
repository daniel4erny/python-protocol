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
        print(Fore.CYAN + f"[i] Database path: {db_path}")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            text TEXT,
            date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)

        print(Fore.LIGHTYELLOW_EX + "[✓] table messages initiated")
        coolDB.commit()
    except Exception as e:
        print(Fore.RED + "[x] an error ocurred while initiating the database")
        print(Fore.RED + f"{e}")

def writeMsg(userName, messageText):
    try:
        cursor.execute("""
            INSERT INTO messages (user, text) 
            VALUES (?, ?)
            """, (userName, messageText))
        coolDB.commit()
        print(Fore.LIGHTYELLOW_EX + f"[✓] zpráva uložena do DB s id {cursor.lastrowid}")
    except Exception as e:
        print(Fore.RED + f"[x] and error occured while saving the message {e}")

def getMsg(idNum):
    try:
        idNum = int(idNum)
        cursor.execute("""SELECT * FROM messages WHERE id = ?""", (idNum,))
        print(Fore.LIGHTYELLOW_EX + "[✓] db fetching message")
        return cursor.fetchall()
    except Exception as e:
        print(Fore.RED + f"[x] and error occured while fetching the message {e}")