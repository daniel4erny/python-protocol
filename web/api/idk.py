from database.db import *

#This API mainly serves as a 
#this is where the request is firstly passed, passes is into other functions based on the method of the request
def handle_reponse_idk(request, query_string):
    first_line = request.splitlines()[0]
    parts = first_line.split(" ")
    method = parts[0].strip()
    if method == "GET":
        return handle_get(request, query_string)
    elif method == "POST":
        return handle_post(request)
    else:
        return "idk what you sent, but its fuckin cool"

#this is called if the method is GET
def handle_get(request, query_string):
    idNumber = str(query_string).replace("id=", "")
    if idNumber.isdigit():
        return getMessage(idNumber, openDB())
    else:
        return f"u fucking dumb or something ? {query_string}"

#this is called if the method is POST and returns the body of the request
def handle_post(request):
    headers, body = request.split("\r\n\r\n", 1)
    response = f"you sent a POST request !!! \n body: {body}"  
    conn = openDB() 
    writeMessage(body, conn)
    return response

 

