import pygame
import argparse
import time
import components.screens as screens
from threading import Thread
from pygame.locals import *
from pygame.sprite import RenderPlain, collide_rect
from components.boards import MainBoard, PlayerBoard, PBoardSide
from client import Client


class Brisca:
    def __init__(self, host):
        self.running = True
        self.display_surf = None
        self.size = self.width, self.height = 1280, 720
        self.screen = None
        self.client = None
        self.client_thread = None
        self.temp = True
        self.host = host

    def on_init(self):
        pygame.init()
        self.display_surf = pygame.display.set_mode(
            self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.running = True
        self.screen = screens.Login(self.login)
        # self.screen = screens.GamingBoard(self.client)

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
            if self.temp:
                time.sleep(2)

            #     cards = ['hearts_2', 'spades_7', 'clubs_11']
            #     for index, card in enumerate(cards):
            #         self.screen.player_boards[0].player = 'gadhi'
            #         self.screen.add_card(card + '.png', 'gadhi', index)
                self.temp = False
        self.on_cleanup()

    def login(self):
        username = self.screen.input.text
        self.client = Client(username=username, host=self.host)
        self.client_thread = Thread(
            target=self.client.start, args=(self.update_state,))
        self.client_thread.start()
        events = self.client.sel.select(timeout=1)
        try:
            key, mask = events[0]
            socket = key.data
            self.client.login(socket)
        except:
            pass

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
            self.screen.player_boards[0].player = self.client.username
            self.screen.player_boards[0].label.text = self.client.username
            self.screen.room = response.get('room')
            players_in_room = response.get('players_in_room')
            if len(players_in_room) > 1:
                m_idx = -(len(players_in_room) + 1)
                boards = self.screen.player_boards[:m_idx:-1]
                for player, board in zip(players_in_room[-2::-1], boards):
                    board.player = player
                    board.label.text = player
        elif status == 'player_entered':
            new_player = response.get('new_player')
            if new_player != self.client.username:
                for board in self.screen.player_boards:
                    if board.player == '(Empty)':
                        board.player = new_player
                        board.label.text = new_player
                        break
        elif status == 'room_ready':
            player_turn = response.get('player')
            cards = response.get('cards')
            triunf = response.get('triunf')
            self.screen.main_board.turn.text = player_turn
            self.screen.main_board.update_triunf(triunf)
            for index, card in enumerate(cards):
                self.screen.add_card(
                    card + '.png', self.client.username, index)
        elif status == 'player_picked_card':
            player_that_picked = response.get('picked')
            next_turn = response.get('next_player')
            self.screen.main_board.turn.text = next_turn
            if player_that_picked != self.client.username:
                card = response.get('card')
                self.screen.add_card(card + '.png', player_that_picked)
        elif status == 'round_finished':
            winner = response.get('winner')
            next_card = response.get('next_card')[0]
            self.screen.add_card(
                next_card + '.png', self.client.username, self.screen.last_picked_index)
            target_board = list(
                filter(lambda x: x.player == winner, self.screen.player_boards))[0]
            for player_board in self.screen.player_boards:
                player_board.selected_card.target_pos = target_board.winns.rect.center
            self.screen.main_board.turn.text = winner

        elif status == 'disconnect':
            socket.close()
            self.running = False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Brisca host.')
    parser.add_argument('-d', dest='host', help='user to use')

    args = parser.parse_args()

    if args.host is None:
        app = Brisca(host='127.0.0.1')
        app.on_execute()
    else:
        app = Brisca(host=args.host)
        app.on_execute()
