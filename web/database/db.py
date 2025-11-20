import sqlite3
from dotenv import load_dotenv
import os
import colorama

# INIT

#colorama
BARVICKA = colorama.Fore.LIGHTYELLOW_EX
RED = colorama.Fore.RED

#.env db path
load_dotenv()
db_path = os.getenv("DATABASE_PATH")
print(db_path)

#openDB initializes database returns connection to work work on API files
def openDB():
    try:
        conn = sqlite3.connect(db_path)
        print(BARVICKA + "DB WORKS EZ PZ")

        cursor = conn.cursor()
        cursor.execute("""
CREATE TABLE IF NOT EXISTS zpravicky(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    zpravy TEXT,
    date DATETIME DEFAULT CURRENT_TIMESTAMP      
    )
""")

        return conn
    except Exception as e:
        print(RED + str(e))

#write message writes the message to db duh >w<
def writeMessage(message, conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
INSERT INTO zpravicky (zpravy)
VALUES (?) 
""", (message,))
        conn.commit()

        print(BARVICKA + f"{message} was sent with id: {cursor.lastrowid}")
    except Exception as e:
        print(RED + str(e))

#This gets the message with id passed as argument
def getMessage(idUnparsed, conn):
    try:
        idParsed = int(idUnparsed)
        cursor = conn.cursor()
        cursor.execute("""
SELECT * FROM zpravicky WHERE id = ?
""", (idParsed,))
        return str(cursor.fetchall())
    except Exception as e:
        print(RED + e)

