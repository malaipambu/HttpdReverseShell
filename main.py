#!/usr/bin/python3
from controller import Controller
import argparse
import socket as s

def main():
    defaultIP=s.gethostbyname(s.gethostname())
    parser = argparse.ArgumentParser(description='Get input for IP and port')
    parser.add_argument('-i', '--ip', metavar='192.168.1.1', help='The IP which the Web Server runs', default=defaultIP)
    args = parser.parse_args()

    obj=Controller(args.ip)

    try:
        obj.start()
    except KeyboardInterrupt:
        print("You Have Closed the service")
    except Exception as e:
        print (str(e))
          
if __name__ == '__main__':
    main()