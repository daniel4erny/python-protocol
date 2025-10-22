# socket is a module for networking
import socket

def ipConfig(): #just info function, making sure everything works
    hostname = socket.gethostname()
    print("Hostname:", hostname)
    print("IP:", socket.gethostbyname(hostname))

#setting the connect info variables and making socekt
def setConnectInfo(): 
    global host, port, s #setting variables global
    host = "127.0.0.1" #(local only)
    port = 5000 #server listens on port 5000
    s = socket.socket() #creating default socket

#function to connect to server
def connection():
    s.connect((host, port)) #connects the socket to the server
    while True: #keeping it runnin
        message = input("Send message: ") #interactive sending 
        s.send(message.encode()) #encoding the message from client to raw bytes
        data = s.recv(1024) #recieving data from server max 1Kb
        print("Server:", data.decode()) #printing response from server

def main():
    ipConfig()
    setConnectInfo()
    connection()

if __name__ == "__main__":
    main()
