import socket             

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
print("socket binded to %s" %(port)) 

s.listen(5)     
print("socket is listening")            

while True: 

    c, addr = s.accept()     
    print('Got connection from', addr )

    data = c.recv(1024)
    parser = HttpParser(data)

    try:
        http_header = """ HTTP/1.1 200
        Content-Type: text/html

        """
        file_name = parser.file.decode("utf-8").replace("/", "")
        file = open(f"./{file_name}", "r").read()
        c.send((http_header + file).encode("utf-8"))
    except:
        error_page = open("./404.html", "r").read()
        error_page_header =  f"""HTTP/1.1 404
        Content-Type: text/html


        """
        c.send((error_page_header+error_page).encode("utf-8"))

    c.close()
