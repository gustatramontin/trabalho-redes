import socket             
import re

class HttpParser:
    def __init__(self, raw):
        lines = raw.split(b"\r\n")
        self.header       = lines[0]
        self.request      = self.header.split(b" ")[0]
        self.file         = self.header.split(b" ")[1]
        self.http_version = self.header.split(b" ")[2]
        self.arguments = {}
        self.parse_lines(lines[1:])


    def parse_line(self, line):
        unpacked = line.split(b": ")
        if (len(unpacked) != 2):
            return None
        header, value = unpacked 
        return header, value 

    def parse_lines(self, lines):
        for line in lines:
            unpacked = self.parse_line(line)
            if (not unpacked):
                continue
            name, value = unpacked
            self.arguments[name] = value

s = socket.socket()         
print("Socket successfully created")

port = 12345               

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', port))         
print(f"socket binded to {port}") 

s.listen(5)     
print("socket is listening")            

while True: 

    c, addr = s.accept()     
    print('Got connection from', addr )

    data = c.recv(1024)

    parser = HttpParser(data)
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    url = parser.file.decode("utf-8")
    domain = re.sub("http://", "", url)
    domain = re.sub("/.*", "", domain)

    client.connect((domain, 80))
    client.send(f"GET {url} HTTP/1.1\n\r\n\r".encode())

    MAX_CONTENT_SIZE = 8*1024
    msg = client.recv(MAX_CONTENT_SIZE)

    c.send(msg)
    c.close()
