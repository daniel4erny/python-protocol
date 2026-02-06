import socket
import ssl
from api.idk import handle_reponse_idk
from api.getAllMessages import getAllMessages
from api.stream import handle_stream_request
from api.sendMessage import handle_send_message
import os
from dotenv import load_dotenv
from utils.logger import console, log, log_request, log_response
from rich.panel import Panel
from rich.text import Text

load_dotenv()

#------------------------------------INIT------------------------------------

#host and port config
hostname = "0.0.0.0"
port = 8443

#paths
index = r"client/html/index.html"
board = r"client/html/board.html"
styles = r"client/css/styles.css"
chat = r"client/html/chat.html"
javascript = r"client/js/main.js"
ezop = r"client/images/ezop.jpg"

#memory of the chat
message_list = []

#paths needed for tls crypting
cert_path = os.getenv("CERT_PATH")
key_path = os.getenv("KEY_PATH")

#loading ssl context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(cert_path, key_path)

#biding socket itself
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((hostname, port))
s.listen(5)
console.print(Panel(Text("server is listening on https://localhost:8443", style="bold green"), title="Server Status"))

#------------------------------------FUNCTIONS------------------------------------

def raw_response(type_str, body):
    response = b"HTTP/1.1 200 OK\r\n" \
               b"Content-Type: " + type_str.encode('utf-8') + b"\r\n" \
               b"Content-Length: " + str(len(body)).encode('utf-8') + b"\r\n\r\n" + body
    return response

def make_response(request, ss, addr):
    first_line = request.splitlines()[0]
    parts = first_line.split(" ")
    method = parts[0]
    
    path = parts[1].strip() if len(parts) >= 2 else "/"
    if ".." in path:
        path = "/"

    if "?" in path:
        path, query_string = path.split("?", 1)
    else:
        query_string = ""
    
    log_request(method, path, addr)

    match path.strip():
        #files responses
        case "/":
            with open(index, "rb") as f: body = f.read()
            return raw_response("text/html", body)
        case "/board.html":
            with open(board, "rb") as f: body = f.read()
            return raw_response("text/html", body)
        case "/chat.html":
            with open(chat, "rb") as f: body = f.read()
            return raw_response("text/html", body)
        case "/styles.css":
            with open(styles, "rb") as f: body = f.read()
            return raw_response("text/css", body)
        case "/ezop.jpg":
            with open(ezop, "rb") as f: body = f.read()
            return raw_response("image/jpeg", body)
        case "/main.js":
            with open(javascript, "rb") as f: body = f.read()
            return raw_response("text/javascript", body)
        #API responses
        case "/api/idk":
            unparsedBody = handle_reponse_idk(request, query_string)
            body = unparsedBody.encode()
            return raw_response("text/plain", body)
        case "/api/getAllMessages":
            unparsedBody = getAllMessages(request)
            body = unparsedBody.encode()
            return raw_response("text/plain", body)
        case "/api/stream":
            # Pass the socket and address correctly for SSE
            handle_stream_request(ss, addr, message_list)
            return None # Important: Signal that response was already handled
        case "/api/sendMessage":
            unparsedBody = handle_send_message(message_list, request)
            body = unparsedBody.encode()
            return raw_response("text/plain", body)
        case _:
            body = b"404 Not Found"
            return raw_response("text/plain", body)

def receive_full_request(ss):
    data = b""
    while True:
        chunk = ss.recv(4096)
        if not chunk:
            break
        data += chunk
        
        # Check if we have headers
        if b"\r\n\r\n" in data:
            headers_part, body_part = data.split(b"\r\n\r\n", 1)
            content_length = 0
            
            # Try to find Content-Length in headers
            for line in headers_part.split(b"\r\n"):
                if line.lower().startswith(b"content-length:"):
                    try:
                        content_length = int(line.split(b":")[1].strip())
                    except ValueError:
                        pass
            
            # If we have the full body, stop reading
            if len(body_part) >= content_length:
                return data.decode('utf-8')
    
    return data.decode('utf-8') if data else None

#------------------------------------MAIN------------------------------------
def connection():
    while True:
        try:
            conn, addr = s.accept()
            with context.wrap_socket(conn, server_side=True) as ss:
                data = receive_full_request(ss)
                
                # Handling empty requests which can happen
                if not data:
                    continue

                response = make_response(data, ss, addr)

                if response:
                    # Parse headers for logging (simple split)
                    headers, _ = response.split(b"\r\n\r\n", 1)
                    first_header = headers.split(b"\r\n")[0].decode('utf-8')
                    
                    # Log successful response
                    log_response(first_header, "unknown (binary)", len(response))
                    
                    ss.sendall(response)
                
        except ssl.SSLError as e:
            console.print(f"[bold red]SSL Error:[/] {e}")
            if "HTTP_REQUEST" in str(e):
                console.print("[yellow]Hint:[/] Use HTTPS -> https://localhost:8443")
        except Exception as e:
            console.print(f"[bold red]Error:[/] {e}")

connection()