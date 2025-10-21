import socket

def initServer():
    global host, port, s
    host = "127.0.0.1"
    port = 5000
    s = socket.socket()
    s.bind((host, port))
    s.listen(1)
    print("Server initiated!!!")

def clientConnect():
    global conn, addr
    conn, addr = s.accept()
    print(f"Připojeno: {addr}")

def aliveServer():
    while True:
        clientConnect()
        while True:
            data = conn.recv(1024)
            if not data:
                print("Klient se odpojil")
                break
            print("Klient:", data.decode())
            conn.send("Odpověď serveru".encode())

def main():
    initServer()
    aliveServer()

if __name__ == "__main__":
    main()
