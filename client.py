import sys
import socket
import selectors
import traceback

import lib

class Client:
    def __init__(self, host='127.0.0.1', port=3000, username='morpheus'):
        self.sel = selectors.DefaultSelector()
        self.addr = (host, port)
        print("starting connection to", self.addr)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(False)
        self.sock.connect_ex(self.addr)
        self.events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.socket = lib.SocketHandler(self.sel, self.sock, self.addr)
        self.sel.register(self.sock, self.events, data=self.socket)
        self.username = username
        self.auth = False
    
    def create_request(self, action, value):
        return dict(
            content=dict(action=action, value=value),
        )

    def evaluate_request(self, socket):
        if not self.auth:
            content = {"action": "login", "value": self.username}
        else:
            input("decime que hacer")
        socket.write(content)
    
    def evaluate_response(self, socket):
        response = socket.response 
        socket.response = None
        if response.get("status") == "ok":
            self.auth = True

    def start(self):
        try:
            while True:
                events = self.sel.select(timeout=1)
                for key, mask in events:
                    socket = key.data
                    try:
                        if mask & selectors.EVENT_WRITE:
                            self.evaluate_request(socket)
                        if mask & selectors.EVENT_READ:
                            socket.read()
                            if socket.response is not None:
                                self.evaluate_response(socket)
                    except Exception:
                        print(
                            "main: error: exception for",
                            f"{socket.addr}:\n{traceback.format_exc()}",
                        )
                        socket.close()
                # Check for a socket being monitored to continue.
                if not self.sel.get_map():
                    break
        except KeyboardInterrupt:
            print("caught keyboard interrupt, exiting")
        finally:
            self.sel.close()


client = Client()
client.start()



