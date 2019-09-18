import pygame
import components.screens as screens
from threading import Thread
from pygame.locals import *
from pygame.sprite import RenderPlain, collide_rect
from components.boards import MainBoard, PlayerBoard, PBoardSide
from client import Client


class Brisca:
    def __init__(self):
        self.running = True
        self.display_surf = None
        self.size = self.width, self.height = 1280, 720
        self.screen = None
        self.client = None
        self.client_thread = None

    def on_init(self):
        pygame.init()
        self.display_surf = pygame.display.set_mode(
            self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.running = True
        self.screen = screens.Login(self.login)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            if self.client is not None:
                self.client.disconnect(self.client.socket)
            else:
                self.running = False
        self.screen.on_event(event)

    def on_loop(self):
        self.screen.update()

    def on_render(self):
        self.display_surf.blit(self.screen.background, (0, 0))
        self.screen.draw(self.display_surf)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self.running = False

        while self.running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def login(self):
        username = self.screen.input.text
        self.client = Client(username=username)
        self.client.login(self.client.socket)
        self.client_thread = Thread(
            target=self.client.start, args=(self.update_state,))
        self.client_thread.start()

    def update_state(self, socket):
        response = socket.response
        status = response.get('status')
        if status == 'error':
            print("ERROR: ", response.get('message'))
        elif status == 'login':
            self.screen = screens.Lobby(self.client)
        elif status == 'room_created':
            self.client.get_rooms(self.client.socket)
        elif status == 'get_rooms':
            if isinstance(self.screen, screens.Lobby):
                self.screen.available_rooms.update_list(response.get('rooms'))
        elif status == 'join_room':
            self.screen = screens.GamingBoard(self.client)
        elif status == 'disconnect':
            socket.close()
            self.running = False


if __name__ == "__main__":
    app = Brisca()
    app.on_execute()
