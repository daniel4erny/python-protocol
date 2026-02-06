import sqlite3
from dotenv import load_dotenv
import os
from utils.logger import console

# INIT
load_dotenv()
db_path = os.getenv("DATABASE_PATH")

#openDB initializes database returns connection to work work on API files
def openDB():
    try:
        conn = sqlite3.connect(db_path)
        # console.print("[dim]DB connected[/]") # Optional: reduce noise

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
        console.print(f"[bold red]DB Error:[/] {e}")

#write message writes the message to db duh >w<
def writeMessage(message, conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
INSERT INTO zpravicky (zpravy)
VALUES (?) 
""", (message,))
        conn.commit()

        console.print(f"[green]DB Insert:[/] {message} (ID: {cursor.lastrowid})")
    except Exception as e:
        console.print(f"[bold red]DB Error:[/] {e}")

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
        console.print(f"[bold red]DB Error:[/] {e}")

#This functions gets all messages
def getAllMessagesDB(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM zpravicky
            ORDER BY id DESC
            LIMIT 10
        """)
        return str(cursor.fetchall())
    except Exception as e:
        console.print(f"[bold red]DB Error:[/] {e}")
