def handle_reponse_idk(request):
    first_line = request.splitlines()[0]
    parts = first_line.split(" ")
    method = parts[0].strip()
    if method == "GET":
        return handle_get(request)
    elif method == "POST":
        return handle_post(request)

def handle_get(request):
    return "you sent a GET request !!!"

def handle_post(request):
    headers, body = request.split("\r\n\r\n", 1)
    response = f"you sent a POST request !!! \n body: {body}"
    return response

 

