# socket is a module for networking
import socket
import time
import sys
import json
import os
from colorama import Fore, Style, init

init(autoreset=True)  # automaticky resetuje barvy po každém výpisu

class Message:
    def __init__(self, userName, text):
        self.userName = userName
        self.text = text

    def toDict(self):
        return {"user": self.userName, "text": self.text}
    
class Packet:
    def __init__(self, method, messageFromUser):
        self.method = method
        self.messageFromUser = messageFromUser

    def toDict(self):
        return {"method": self.method, "message": self.messageFromUser}

def clear():
    # pro Windows
    if os.name == 'nt':
        os.system('cls')
    # pro Linux/macOS
    else:
        os.system('clear')

# MAKING PACKET TO SEND ------------------------------------------------------------------------------
def setMethod():
    print(Fore.CYAN + f"type [1] for writing into database")
    print(Fore.CYAN + f"type [2] for fetching message")
    userInput = input(Fore.CYAN + f"set method: ")
    if int(userInput) == 1:
        return("WRITE")
    elif int(userInput) == 2:
        return("GET")
    else:
        print(Fore.RED + f"[x] input 1 or 2!")
        return setMethod()

def makeMsg():
    userNameInput = input(Fore.YELLOW + "Set your signature: ")    
    textInput = input(Fore.YELLOW + "Type your message: ")
    passInput = input(Fore.YELLOW + "Press set password for the message (this will be needed to fetch it): ")
    messageToSend = Message(userNameInput, textInput)
    if not textInput.strip():
        print(Fore.RED + "[x] you can't send empty message!")
        return makeMsg()
    else:
        return messageToSend

def getMsg():
    idInput = input(Fore.YELLOW + f"type the id of message you want to receive: ")
    if not idInput.strip():
        print(Fore.RED + f"[x] you cant get message with empty ID!")
        return getMsg()
    else:
        return idInput
    
def makePacket():
    try:
        method = setMethod()
        clear()
        if method == "GET":
            packetToSend = Packet(method, getMsg())
        elif method == "WRITE":
            packetToSend = Packet(method, makeMsg().toDict())
        else:
            print(Fore.RED + "[x] making packet failed, try again")
            time.sleep(1)
            clear()
            return makePacket()
        packetToSend = json.dumps(packetToSend.toDict())
        print(packetToSend)
        return packetToSend
    except Exception as e:
        print(Fore.RED + f"[x] an error occured {e}")
# ----------------------------------------------------------------------------------------------------
def ipConfig():  # just info function, making sure everything works
    hostname = socket.gethostname()
    print(Fore.CYAN + "Hostname:", Fore.WHITE + hostname)
    print(Fore.CYAN + "IP:", Fore.WHITE + socket.gethostbyname(hostname))


# setting the connect info variables and making socket
def setConnectInfo():
    global host, port, s  # setting variables global
    host = "127.0.0.1"  # (local only)
    port = 5000  # server listens on port 5000
    s = socket.socket()  # creating default socket
    print(Fore.GREEN + f"[OK] Socket created. Connecting to {host}:{port}...")


def sendPass():
    password = input(Fore.YELLOW + "Type password: " + Style.RESET_ALL)
    s.send(password.encode())
    passStatus = s.recv(1024).decode()

    if passStatus == "correct":
        print(Fore.GREEN + "[ACCESS GRANTED] Correct password!")
    else:
        print(Fore.RED + "[ACCESS DENIED] Incorrect password. Script will terminate...")
        time.sleep(3)
        sys.exit()


# function to connect to server
def connection():
    try:
        s.connect((host, port))  # connects the socket to the server
        print(Fore.GREEN + "[CONNECTED] Connected to server successfully!")
    except ConnectionRefusedError:
        print(Fore.RED + "[ERROR] Cannot connect to server. Make sure it is running.")
        sys.exit()

    sendPass()
    while True:  # keeping it running
        packet = makePacket()
        if not packet.strip():
            print(Fore.RED + "[INFO] Empty packet, cannot send empty message")
            time.sleep(1)
            clear()
            continue
        else:
            s.send(packet.encode())  # encoding the message
            data = s.recv(1024)  # receiving data from server max 1Kb
            print(Fore.BLUE + "Server:", Style.RESET_ALL + data.decode())


def main():
    ipConfig()
    setConnectInfo()
    connection()


if __name__ == "__main__":
    main()
