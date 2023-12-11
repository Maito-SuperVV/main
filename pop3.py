from socket import *
import os
import re
import json
from email import message_from_string
import email
from pathlib import Path
BUFFER_SIZE=1024

parent_path="D:/Python_Store/pop3_client"

def Check_Exist_msg(msg_name,folder_paths):
    for str in folder_paths:
        msg_path=os.path.join(str,msg_name)
        if Path(msg_path).exist():
            return True
    return False

def receive_rawEmail(clientSocket):
    raw_email=b''
    while True:
        data_temp=clientSocket.recv(BUFFER_SIZE)
        raw_email+=data_temp
        if b'\r\n.\r\n' in data_temp:
            break       
    raw_email=raw_email.decode("utf8")
    pos_first_n=raw_email.find("\r\n")+len("\r\n")
    raw_email = raw_email[pos_first_n:]
    return raw_email

def determine_Path(froM, subject, content, msg_name, pair_from, pair_subject, pair_content, pair_spam):
    if froM in pair_from_folder[0]:
        path=os.path.join("D:/Python_Store",pair_from[1]) 
        return os.path.join(path,msg_name) 
    for str in pair_subject[0]:
        if(str in subject):
            path=os.path.join("D:/Python_Store",pair_subject[1])
            return os.path.join(path,msg_name)
    for str in pair_content[0]:
        if str in content:
            path=os.path.join("D:/Python_Store",pair_content[1])
            return os.path.join(path,msg_name)    
    for str in pair_spam[0]:
        if (str in content) or (str in subject):
            path=os.path.join("D:/Python_Store",pair_spam[1])
            return os.path.join(path,msg_name)
    return os.path.join("D:/Python_Store/Inbox",msg_name)

def Get_TextBody_msg(msg):
    if not msg.is_multipart():
        return msg.get_payload(decode=True).decode(msg.get_content_charset(),'ignore')
    for part in msg.walk():
        Content_Type=part.get_content_type()
        if Content_Type=='text/plain':
            return part.get_payload(decode=True).decode(part.get_content_charset(),'ignore')

def Download_msgFile(order,msg_name,folder_path,clientSocket,pair_from,pair_subject,pair_content,pair_spam):
    clientSocket.sendall("RETR {}\r\n".format_map(order).encode())
    raw_email=receive_rawEmail(clientSocket)
    msg=message_from_string(raw_email)
    froM=msg.get("From")
    subject=msg.get("Subject")
    content=Get_TextBody_msg(msg)
    path_To_save=determine_Path(froM,subject,content,msg_name,pair_from,pair_subject,pair_content,pair_spam)
    file=open(path_To_save,'r')
    file.read(raw_email)
    file.close()

def Get_folder_path(parent_path,from_folder,subject_folder,content_folder,spam_folder):
    folder_path=[]
    t=os.path.join(parent_path,"Inbox")
    if not Path(t).exists():
        Path(t).mkdir()
    folder_path.append(t)
    t=os.path.join(parent_path,from_folder)
    if not Path(t).exists():
        Path(t).mkdir()
    folder_path.append(t)
    t=os.path.join(parent_path,subject_folder)
    if not Path(t).exists():
        Path(t).mkdir()
    folder_path.append(t)
    t=os.path.join(parent_path,content_folder)
    if not Path(t).exists():
        Path(t).mkdir()
    folder_path.append(t)
    t=os.path.join(parent_path,spam_folder)
    if not Path(t).exists():
        Path(t).mkdir()
    folder_path.append(t)
    return folder_path

def Get_list_msg(UIDL):
    while 1:
        print(1)

#Read File Config Start
f=open("D:/Python_Store/pop3_client/filter_Congif.json","r")
filters=json.load(f)['Filter']
pair_from_folder=(filters[0]["From"],filters[0]["ToFolder"])
pair_subject_folder=(filters[1]["Subject"],filters[1]["ToFolder"])
pair_content_folder=(filters[2]["Content"],filters[2]["ToFolder"])
pair_spam_folder=(filters[3]["Spam"],filters[3]["ToFolder"])
f.close()
#Read File Config End
folder_paths=Get_folder_path(parent_path,pair_from_folder[1],pair_subject_folder[1],pair_content_folder[1],pair_spam_folder[1])
user_email="nqvinhdongthap322004@gmail.com"
user_pass="vinhdeptrai"
host='127.0.0.1'
port=3335
clientSocket=socket(AF_INET,SOCK_STREAM)
clientSocket.connect((host,port))
clientSocket.recv(BUFFER_SIZE)
clientSocket.sendall("CAPA\r\n".encode())
clientSocket.recv(BUFFER_SIZE)
clientSocket.sendall("USER {}\r\n".format(user_email).encode())
clientSocket.recv(BUFFER_SIZE)
clientSocket.sendall("PASS {}\r\n".format(user_pass).encode())
clientSocket.recv(BUFFER_SIZE)
clientSocket.sendall("STAT\r\n".encode())
rev1=clientSocket.recv(BUFFER_SIZE).decode()
if(rev1[:5]=='OK 0 0'):
    clientSocket.send("QUIT\r\n".encode())
    clientSocket.close()
clientSocket.sendall("LIST\r\n".encode())
clientSocket.recv(1024) #OK
clientSocket.sendall("UIDL\r\n".encode())
recv_UIDL=clientSocket.recv(BUFFER_SIZE)
list_msg=Get_list_msg(recv_UIDL)
clientSocket.send("QUIT\r\n".encode())
clientSocket.close()
