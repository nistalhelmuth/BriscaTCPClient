import sys
import socket
import selectors
import traceback
import argparse

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

    def evaluate_request(self, socket):
        if not self.auth:
            self.login(socket)
            return
        else:
            print("TEST MENU")
            print("1. get_rooms")
            print("2. create_room")
            print("3. join_room")
            print("4. get_players")
            print("5. disconnect")
            option = input()
            if option == "1":
                self.get_rooms(socket)
            elif option == "2":
                self.create_room(socket, "new room")
            elif option == "3":
                self.join_room(socket, "new room")
            elif option == "4":
                self.get_players(socket)
            elif option == "5":
                self.disconnect(socket)

    def login(self, socket):
        socket.write({"action": "login", "user": self.username})

    def create_room(self, socket, room):
        socket.write({"action": "create_room",
                      "user": self.username, "room": room})

    def join_room(self, socket, room):
        socket.write({"action": "create_room",
                      "user": self.username, "room": room})

    def get_rooms(self, socket):
        socket.write({"action": "get_rooms", "user": self.username})

    def get_players(self, socket):
        socket.write({"action": "get_players", "user": self.username})

    def disconnect(self, socket):
        socket.write({"action": "disconnect", "user": self.username})

    def evaluate_response(self, socket):
        response = socket.response
        socket.response = None
        status = response.get("status")
        if status == "error":
            print("ERROR: ", response.get("message"))
            if not self.auth:
                print("connection closed")
                socket.close()
        elif status == "login":
            print("Current players:", response.get("players"))
            print("Current rooms:", response.get("rooms"))
            self.auth = True
        elif status == "get_rooms":
            print("Current rooms:", response.get("rooms"))
        elif status == "create_room":
            print("Current rooms:", reponse.get("rooms"))
        elif status == "join_room":
            print("Current players in ", response.get("room"))
            print(response.get("players_in_room"))
        elif status == "get_players":
            print("Current players:", response.get("players"))
        elif status == "disconnect":
            print("connection disconnected")
            socket.close()

    def start(self, gui_listener=None):
        try:
            while True:
                events = self.sel.select(timeout=1)
                for key, mask in events:
                    socket = key.data
                    try:
                        if mask & selectors.EVENT_WRITE and gui_listener is None:
                            self.evaluate_request(socket)
                        if mask & selectors.EVENT_READ:
                            socket.read()
                            if socket.response is not None:
                                if gui_listener is None:
                                    self.evaluate_response(socket)
                                else:
                                    gui_listener(socket)
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Brisca client.')
    parser.add_argument('-u', dest='user', help='user to use')

    args = parser.parse_args()

    if args.user is None:
        client = Client()
        client.start()
    else:
        client = Client(username=args.user)
        client.start()
