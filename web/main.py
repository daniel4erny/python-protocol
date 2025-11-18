import socket
import ssl
import colorama
from api.idk import handle_reponse

# colorama
RED = colorama.Fore.RED
GREEN = colorama.Fore.GREEN
BLUE = colorama.Fore.LIGHTBLUE_EX
YELLOW = colorama.Fore.YELLOW

hostname = "localhost"
port = 8443
index = r"client/index.html"
styles = r"client/styles.css"
javascript = r"client/main.js"
ezop = r"client/ezop.jpg"

cert_path = "cert.pem"
key_path = "key.pem"
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(cert_path, key_path)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((hostname, port))
s.listen(5)
print(GREEN + "----------- socket is listening -----------")

def raw_response(type_str, body):
    response = b"HTTP/1.1 200 OK\r\n" \
               b"Content-Type: " + type_str.encode('utf-8') + b"\r\n" \
               b"Content-Length: " + str(len(body)).encode('utf-8') + b"\r\n\r\n" + body
    return response

def make_response(request):
    first_line = request.splitlines()[0]
    parts = first_line.split(" ")

    path = parts[1].strip() if len(parts) >= 2 else "/"
    if ".." in path:
        path = "/"

    match path:
        case "/":
            with open(index, "rb") as f:
                body = f.read()
            return raw_response("text/html", body)
        case "/styles.css":
            with open(styles, "rb") as f:
                body = f.read()
            return raw_response("text/css", body)
        case "/ezop.jpg":
            with open(ezop, "rb") as f:
                body = f.read()
            return raw_response("image/jpeg", body)
        case "/main.js":
            with open(javascript, "rb") as f:
                body = f.read()
            return raw_response("text/javascript", body)
        case "/api/idk":
            unparsedBody = handle_reponse()
            body = unparsedBody.encode()
            return raw_response("text/plain", body)
        case _:
            body = b"404 Not Found"
            return raw_response("text/plain", body)



            


def connection():
    while True:
        try:
            conn, addr = s.accept()
            print(GREEN + f"Connection from {addr}")
            with context.wrap_socket(conn, server_side=True) as ss:
                data = ss.recv(50000).decode('utf-8')
                print(YELLOW + "-------------------------- START OF REQUEST -----------------------")
                print(BLUE + data)
                print(YELLOW + "-------------------------- END OF REQUEST -----------------------")

                response = make_response(data)

                # --- ZMĚNA ZDE ---
                
                # Oddělíme hlavičky od těla binární odpovědi
                headers, body_bin = response.split(b"\r\n\r\n", 1)
                
                # Vytiskneme hlavičky (jako text) a informaci o těle (jako délku)
                print("\r")
                print("\r")
                print(YELLOW + "-------------------------- START OF RESPONSE -----------------------")
                print(BLUE + headers.decode("utf-8")) # Tiskneme pouze hlavičky
                print(BLUE + f"(Binární tělo o délce: {len(body_bin)} bajtů)")
                print(YELLOW + "-------------------------- END OF RESPONSE -----------------------")
                
                # --- ODESÍLÁNÍ ZŮSTÁVÁ SPRÁVNÉ ---
                ss.sendall(response) # Odeslání celé binární odpovědi
                ss.close()

        except Exception as e:
            # Vaše původní chybová hláška SSL byla způsobena nedokončeným požadavkem/odpovědí.
            # Po této opravě by měla být stabilnější.
            print(RED + f"{e}")

connection()