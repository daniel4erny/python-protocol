# socket is a module for networking
import socket

#function to intialize the server
def initServer():
    global host, port, s #setting important variables as global
    host = str("127.0.0.1") #localhost (will change)
    port = int(5000) #setting the port to 5000
    s = socket.socket() #setting socket in variable
    s.bind((host, port)) #making socket listen on host and port
    s.listen(1) #server listens only onto one socket that is connected to it
    print("Server initiated!!!") #just info messages
    print(s)
    print(f"HOST: {host}, PORT: {port}")

#function for making client able to connect
def clientConnect():
    global conn, addr #setting clients address and port as global variables
    conn, addr = s.accept() #accepting connection and storing the connection info
    print(f"Connected: {addr}") #info message

#keeping server "alive"
def aliveServer():
    while True: #making it keep running
        clientConnect() #making client
        while True: #keeping he connection with client alive
            data = conn.recv(1024) #receiving data from client max 1Kb
            if not data: 
            #upon disconnectikng data is set to b"" which is assigned to false, making the not data == True
                print("client dissconected") #info msg
                break #breaking the loop upon disconecting
            print("Klient:", data.decode()) #show clients msg
            conn.send("Odpověď serveru".encode()) #anwser client

#main function 
def main(): 
    initServer() #initialization
    aliveServer() #making server run

if __name__ == "__main__": 
    main() #turning it on
