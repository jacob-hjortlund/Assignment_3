import socket
from datetime import datetime, timezone

class server():

    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM

    def __init__(self, host, port):
        self.host = host
        self.port = port
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
        request_line = text.splitlines()[0].rstrip('\r\n')
        self.request, self.path, self.HTTP_ver = request_line.split()
    
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
        connection = "Connection: close\r\n"

        return status_line+date+connection

    def GET_respone(self, blablbala):
        # has to parse encoding etc etc from request
        return 1

    def handle_request(self):
        # TODO: Handle GET request, otherwise return error blablbal
        return 1