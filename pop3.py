from socket import *
import os
import re
import json

parent_path="D:/Python_Store"

def Check_Exist_msg(msg_name,folder_path):
    for str in folder_path:
        msg_path=os.path.join(str,msg_name)
        if msg_path.exist():
            return True
    return False

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
    #content
    #spam

def Download_msgFile(order,msg_name,folder_path,clientSocket,pair_from,pair_subject,pair_content,pair_spam):
    clientSocket.sendall("RETR {}".format_map(order).encode())
    boundary=clientSocket.recv(1024).decode()
    mime_version=clientSocket.recv(1024).decode()
    msg_id=clientSocket.recv(1024).decode()
    date=clientSocket.recv(1024).decode()
    user_agent=clientSocket.recv(1024).decode()
    to=clientSocket.recv(1024).decode()
    froM=re.search(r'<([^>]+)>',clientSocket.recv(1024).decode()).group(1)
    subject=clientSocket.recv(1024).decode()[10:] #? check \r\n in last
    content="msg"
    path_To_save=determine_Path(froM,subject,content,msg_name,pair_from,pair_subject,pair_content,pair_spam)

def Get_folder_path():
    folder_path=[]
    folder_path.append(os.path.join(parent_path,pair_from_folder[1]))
    folder_path.append(os.path.join(parent_path,pair_subject_folder[1]))
    folder_path.append(os.path.join(parent_path,pair_content_folder[1]))
    folder_path.append(os.path.join(parent_path,pair_spam_folder[1]))
    return folder_path

f=open("D:/Python_Store/pop3_client/filter_Congif.json","r")
filters=json.load(f)['Filter']
pair_from_folder=(filters[0]["From"],filters[0]["ToFolder"])
pair_subject_folder=(filters[1]["Subject"],filters[1]["ToFolder"])
pair_content_folder=(filters[2]["Content"],filters[2]["ToFolder"])
pair_spam_folder=(filters[3]["Spam"],filters[3]["ToFolder"])
f.close()
folder_paths=Get_folder_path(parent_path,pair_from_folder[1],pair_subject_folder[1],pair_content_folder[1],pair_spam_folder[1])
user_email="nqvinhdongthap322004@gmail.com"
user_pass="vinhdeptrai"
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
    order=rev[:1]
    if Check_Exist_msg(msg_name,folder_paths,clientSocket)==False:
        Download_msgFile(msg_name,folder_paths)


clientSocket.send("QUIT".encode())
clientSocket.close()
