from database.db import *

def getAllMessages(request):
    first_line = request.splitlines()[0]
    parts = first_line.split(" ")
    method = parts[0].strip()
    if method == "GET":
        return getAllMessagesDB(openDB())
    else:
        return "can only GET !!!!!!"