import socket

def ipConfig():
    hostname = socket.gethostname()
    print("Hostname:", hostname)
    print("IP:", socket.gethostbyname(hostname))

def setConnectInfo():
    global host, port, s
    host = "127.0.0.1"
    port = 5000
    s = socket.socket()

def connection():
    s.connect((host, port))
    while True:
        message = input("Send message: ")
        s.send(message.encode())
        data = s.recv(1024)
        print("Server:", data.decode())

def main():
    setConnectInfo()
    ipConfig()
    connection()

if __name__ == "__main__":
    main()
