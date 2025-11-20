import socket
import ssl
import colorama
from api.idk import handle_reponse_idk
from api.getAllMessages import getAllMessages

#------------------------------------INIT------------------------------------

# colorama init
RED = colorama.Fore.RED
GREEN = colorama.Fore.GREEN
BLUE = colorama.Fore.LIGHTBLUE_EX
YELLOW = colorama.Fore.YELLOW

#host and port config
hostname = "localhost"
port = 8443

#paths needed for HTML site itself
index = r"client/html/index.html"
board = r"client/html/board.html"
styles = r"client/css/styles.css"
javascript = r"client/js/main.js"
ezop = r"client/images/ezop.jpg"

#paths needed for tls crypting
cert_path = r"cert.pem"
key_path = r"key.pem"

#loading ssl context, we will wrap socket with this after
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(cert_path, key_path)

#biding socket itself
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((hostname, port))
s.listen(5)
print(GREEN + "----------- socket is listening -----------")

#------------------------------------FUNCTIONS------------------------------------

#this functions returns the formated http packet, you have to pass type of the request and body
def raw_response(type_str, body):
    response = b"HTTP/1.1 200 OK\r\n" \
               b"Content-Type: " + type_str.encode('utf-8') + b"\r\n" \
               b"Content-Length: " + str(len(body)).encode('utf-8') + b"\r\n\r\n" + body
    return response

#This function handles the request and returns response to it (via previous function), the return is based on the path in request
def make_response(request):
    #here it extracts the first line
    first_line = request.splitlines()[0]
    parts = first_line.split(" ")

    #if parts doesnt have at least two elements we will make the index return and checks for malicous activity trying to get higher in the working directory
    path = parts[1].strip() if len(parts) >= 2 else "/"
    if ".." in path:
        path = "/"

    #Here we split path and query string, only if ? is present
    if "?" in path:
        path, query_string = path.split("?", 1)
    else:
        query_string = ""

    #here we have a switch statement, with each path returning something else, if the path isnt found, it returns 404 error
    match path.strip():
        #files responses
        case "/": #the index return
            with open(index, "rb") as f:
                body = f.read()
            return raw_response("text/html", body)
        case "/board.html":
            with open(board, "rb") as f:
                body = f.read()
            return raw_response("text/html", body)
        case "/styles.css": #styles return
            with open(styles, "rb") as f:
                body = f.read()
            return raw_response("text/css", body)
        case "/ezop.jpg": #image return
            with open(ezop, "rb") as f:
                body = f.read()
            return raw_response("image/jpeg", body)
        case "/main.js": #js file return
            with open(javascript, "rb") as f:
                body = f.read()
            return raw_response("text/javascript", body)
        #API responses
        case "/api/idk": #just testing, mainly serves as a prototype for other api
            unparsedBody = handle_reponse_idk(request, query_string)
            body = unparsedBody.encode()
            return raw_response("text/plain", body)
        case "/api/getAllMessages":
            unparsedBody = getAllMessages(request)
            body = unparsedBody.encode()
            return raw_response("text/plain", body)
        #if not found
        case _:
            body = b"404 Not Found"
            return raw_response("text/plain", body)

#------------------------------------MAIN------------------------------------
def connection():

    #We declare a while true loop so it doesnt crash after exception, and works indefinitely
    while True:
        try:
            #Here we accept the connection and wrap it in ssl context, making it TLS
            conn, addr = s.accept()
            print(GREEN + f"Connection from {addr}")
            with context.wrap_socket(conn, server_side=True) as ss:
                #here we recieve max 50000 bytes and print it
                data = ss.recv(50000).decode('utf-8')
                print(YELLOW + "-------------------------- START OF REQUEST -----------------------")
                print(BLUE + data)
                print(YELLOW + "-------------------------- END OF REQUEST -----------------------")

                #here we pass the whole request into make_response(), which returns the response duh >w<
                response = make_response(data)

                #for the console to be at least readable, we dont print the whole body, only the length of it
                headers, body_bin = response.split(b"\r\n\r\n", 1)
                
                #here we print the response
                print("\r")
                print("\r")
                print(YELLOW + "-------------------------- START OF RESPONSE -----------------------")
                print(BLUE + headers.decode("utf-8")) # Tiskneme pouze hlavičky
                print(BLUE + f"(Binární tělo o délce: {len(body_bin)} bajtů)")
                print(YELLOW + "-------------------------- END OF RESPONSE -----------------------")
                
                #here we send and close connection
                ss.sendall(response)
                ss.close()

        except Exception as e:
            #end of try loop
            print(RED + f"{e}")

#here we start the connection loop
connection()