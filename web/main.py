import socket
import ssl
import colorama

# colorama
RED = colorama.Fore.RED
GREEN = colorama.Fore.GREEN
BLUE = colorama.Fore.LIGHTBLUE_EX
YELLOW = colorama.Fore.YELLOW

hostname = "localhost"
port = 8443
index = "index.html"
styles = "styles.css"

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

    path = parts[1] if len(parts) >= 2 else "/"
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
        case _:  # fallback
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

                print("\r")
                print("\r")
                print(YELLOW + "-------------------------- START OF RESPONSE -----------------------")
                print(BLUE + response.decode("utf-8"))
                print(YELLOW + "-------------------------- END OF RESPONSE -----------------------")

                ss.sendall(response)
                ss.close()

        except Exception as e:
            print(RED + f"{e}")

connection()
