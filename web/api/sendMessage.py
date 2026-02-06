from utils.logger import console

def handle_send_message(messages_list, request):
    headers, body = request.split("\r\n\r\n", 1)
    method = headers.split(" ")[0].strip()
    if method == "POST":
        return handle_post(body, messages_list)
    else:
        console.print("[bold yellow]Warning:[/] Invalid method for sendMessage (not POST)")
        return "Brotha its called sendMessage, tf u mean you are not sending a post request?"

def handle_post(body, messages_list):
    messages_list.append(body.strip())
    console.print(f"[bold magenta]Message Added:[/] '{body.strip()}'")
    return f"'{body.strip()}' was added to the list"
