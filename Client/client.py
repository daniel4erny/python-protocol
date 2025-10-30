# socket is a module for networking
import socket
import time
import sys
import json
import os
import packet as packetMaking
from colorama import Fore, Style, init

init(autoreset=True)  # automaticky resetuje barvy po každém výpisu

def clear():
    # pro Windows
    if os.name == 'nt':
        os.system('cls')
    # pro Linux/macOS
    else:
        os.system('clear')

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
        packet = packetMaking.makePacket()
        if not packet.strip():
            print(Fore.RED + "[INFO] Empty packet, cannot send empty message")
            time.sleep(1)
            clear()
            continue
        else:
            s.send(packet.encode())  # encoding the message
            data = s.recv(1024)  # receiving data from server max 1Kb
            print(Fore.BLUE + "Server:", Style.RESET_ALL + str(json.loads(data.decode())))


def main():
    ipConfig()
    setConnectInfo()
    connection()


if __name__ == "__main__":
    main()
