# socket is a module for networking
import socket
import hashlib
import database
from colorama import Fore, Style, init

init(autoreset=True)  # automaticky resetuje barvy po každém výpisu


#function to intialize the server
def initServer():
    global host, port, s #setting important variables as global
    database.openDb()
    host = str("127.0.0.1") #localhost (will change)
    port = int(5000) #setting the port to 5000
    s = socket.socket() #setting socket in variable
    s.bind((host, port)) #making socket listen on host and port
    s.listen(1) #server listens only onto one socket that is connected to it
    print(Fore.GREEN + "[✓] Server initiated!!!") #just info messages
    print(Fore.YELLOW + str(s))
    print(Fore.CYAN + f"HOST: {host}, PORT: {port}")


#function for making client able to connect
def clientConnect():
    global conn, addr #setting clients address and port as global variables
    conn, addr = s.accept() #accepting connection and storing the connection info
    print(Fore.MAGENTA + f"Connected: {addr}") #info message


def passwordCheck():
    global password #setting password global
    password = "955db0b81ef1989b4a4dfeae8061a9a6" #Hashed by md5 string "heslo"
    clientPassword = conn.recv(1024)
    hashed = hashlib.md5(clientPassword).hexdigest()
    if hashed == password:
        conn.send("correct".encode())
        print(Fore.GREEN + f"[ACCESS GRANTED] Client {addr} provided correct password.")
        return True
    else:
        conn.send("incorrect".encode())
        print(Fore.RED + f"[ACCESS DENIED] Client {addr} provided wrong password, disconnected.")
        conn.close()  # odpojí klienta
        return False


#keeping server "alive"
def aliveServer():
    while True:
        clientConnect()
        if not passwordCheck():  # pokud špatné heslo
            continue  # čeká na další klienta
        else:
            print(Fore.GREEN + f"Client {addr} authenticated successfully!") 
        while True:
            data = conn.recv(1024)
            if not data:
                print(Fore.YELLOW + "Client disconnected")
                break
            print(Fore.BLUE + "Klient: " + Style.RESET_ALL + data.decode())
            conn.send("Odpověď serveru".encode())


#main function 
def main(): 
    initServer() #initialization
    aliveServer() #making server run


if __name__ == "__main__": 
    main() #turning it on
