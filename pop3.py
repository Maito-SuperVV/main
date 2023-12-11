from socket import *
import os
import re
import json
from email import message_from_string
import email
BUFFER_SIZE=1024

parent_path="D:/Python_Store"

def Check_Exist_msg(msg_name,folder_path):
    for str in folder_path:
        msg_path=os.path.join(str,msg_name)
        if msg_path.exist():
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

def Get_folder_path(parent_path,pair_from_folder,pair_subject_folder,pair_content_folder,pair_spam_folder):
    folder_path=[]
    folder_path.append(os.path.join(parent_path,pair_from_folder[1]))
    folder_path.append(os.path.join(parent_path,pair_subject_folder[1]))
    folder_path.append(os.path.join(parent_path,pair_content_folder[1]))
    folder_path.append(os.path.join(parent_path,pair_spam_folder[1]))
    return folder_path
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
clientSocket=socket(AF_INET,SOCK_STREAM)
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
while (rev := clientSocket.recv(1024)) != b'.':
    msg_name=rev[2:]
    order=rev[:1]
    if Check_Exist_msg(msg_name,folder_paths,clientSocket)==False:
        Download_msgFile(msg_name,folder_paths)

clientSocket.send("QUIT\r\n".encode())
clientSocket.close()
