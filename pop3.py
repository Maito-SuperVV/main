from socket import *
import os

def Create_folder():
    folder_name=["Inbox","Project","Important","Work","Spam"]
    folder_path=[]
    for str in folder_name:
        path_to_folder = "D:/Python_Store"
        t = os.path.join(path_to_folder,str)
        folder_path.append(t)
        if not os.path.exists(t):
            os.makedirs(t)
    return folder_path
def Check_BeenRead_Mess(msg_name,folder_path):
    for str in folder_path:
        msg_path=os.path.join(str,msg_name)
        if msg_path.exist():
            return True
    return False

def Download_msgFile(msg_name,folder_path,clientSocket):
    clientSocket

user_email="nqvinhdongthap322004@gmail.com"
user_pass="vinhdeptrai"
folder_path=Create_folder()
clientSocket=socket(AF_INET,SOCK_STREAM)
clientSocket.recv()
clientSocket.sendall("CAPA".encode())
clientSocket.recv()
clientSocket.sendall("USER {}".format(user_email).encode())
clientSocket.recv()
clientSocket.sendall("PASS {}".format(user_pass).encode())
clientSocket.recv()
clientSocket.sendall("STAT".encode())
rev1=clientSocket.recv(1024).decode()
if(rev1[:5]=='OK 0 0'):
    clientSocket.send("QUIT".encode())
    clientSocket.close()
clientSocket.sendall("LIST".encode())
clientSocket.recv(1024) #OK
while (rev := clientSocket.recv(1024)) != b'.':
    msg_name=rev[2:]
    order=rev[:2]
    if (flag:=Check_BeenRead_Mess(msg_name,folder_path,clientSocket)==False):
        Download_msgFile(msg_name,folder_path)


clientSocket.send("QUIT".encode())
clientSocket.close()
