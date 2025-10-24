import time
import json
from colorama import Fore, Style, init
import os

init(autoreset=True)  # automaticky resetuje barvy po každém výpisu

def clear():
    # pro Windows
    if os.name == 'nt':
        os.system('cls')
    # pro Linux/macOS
    else:
        os.system('clear')

class Message:
    def __init__(self, userName, text, password):
        self.userName = userName
        self.text = text
        self.password = password

    def toDict(self):
        return {"user": self.userName, "text": self.text, "password": self.password}
    
class Packet:
    def __init__(self, method, messageFromUser):
        self.method = method
        self.messageFromUser = messageFromUser

    def toDict(self):
        return {"method": self.method, "message": self.messageFromUser}
    
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
    messageToSend = Message(userNameInput, textInput, passInput)
    if not textInput.strip():
        print(Fore.RED + "[x] you can't send empty message!")
        return makeMsg()
    else:
        return messageToSend

def getMsg():
    idInput = input(Fore.YELLOW + f"type the password of message you want to receive: ")
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