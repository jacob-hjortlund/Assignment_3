import socket
import os
from datetime import datetime, timezone
from mako.template import Template
from mimetypes import guess_type


class server():

    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.status = "200 OK"
        self.listen_socket = listen_socket = socket.socket(address_family, socket_type)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_socket.bind((host, port))
        listen_socket.listen()

    def run_server(self):
        listen_socket = self.listen_socket
        while True:
            self.conn, self.addr = listen_socket.accept()
            self.handle_request()

    def parse_HTTP_request(self, text):
        request_split = text.splitlines()
        request_line = request_split[0].rstrip('\r\n')
        self.request, self.path, self.HTTP_ver = request_line.split()
        try:
            self.request_headers = request_split[1:]
        except:
            self.status = "400 Bad Request"

    def listing(self):
        contents = os.listdir("." + self.path)
        template = """
            <html>
            <head>
                <title> Results </title>
            </head>
            <body>
            % for doc in docs:
                <a href="http://localhost:${port}/${doc}"> ${doc} </a>
            % endfor
            </body>
            </html>
            """
        return Template(template).render(docs=contents, port=self.port)

    def check_request(self):
        if self.request != "GET":
            self.status = "404 Not Found"
        if not os.path.exists(self.path):
            self.status = "404 Not Found"
        if self.status != "400 Bad Request":
            if "Host: localhost" not in self.request_headers:
                self.status = "400 Bad Request"

    def _http_date(self):
        dt = datetime.now(tz=timezone.utc)

        weekday = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][dt.weekday()]
        month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
                 'Sep', 'Oct', 'Nov', 'Dec'][dt.month-1]
        
        return f"{weekday}, {dt.day:02d} {month} {dt.year:04d} {dt.hour:02d}:{dt.minute:02d}:{dt.second:02d} GMT"

    def start_response(self, status):
        # Generate status line and general headers of response
        status_line = f"HTTP/1.1 {status}\r\n"
        date = self._http_date() + "\r\n"

        return status_line+date

    def GET_response(self):
        if os.path.isdir(self.path):
            if "index.html" in os.listdir(self.path):
                body = 1#load file
            else:
                body = self.listing()
        return 1

    def handle_request(self):
        # TODO: Handle GET request, otherwise return error blablbal
        http_request = self.conn.recv(1024)
        self.http_request = http_request = http_request.decode('utf-8')
        self.parse_HTTP_request(http_request)
        self.check_request()

        response = self.start_response(self.status)
        if self.status == "200 OK":
            self.GET_response()
        connection = "Connection: close\r\n"
        response += "\r\n"
        response_bytes = response.encode()
        self.conn.sendall(response_bytes)
        self.conn.close()

        return 1