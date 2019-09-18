import pygame.display as display
from pygame import MOUSEBUTTONDOWN, KEYDOWN
from pygame.sprite import RenderPlain, Rect
from utils.loaders import load_image
from .boards import MainBoard, PlayerBoard, PBoardSide
from .ui import Button, Label, TextInput, UIList
from .card import Card


class Screen(RenderPlain):
    def __init__(self):
        RenderPlain.__init__(self)
        display_surf = display.get_surface()
        d_width = display_surf.get_width()
        d_heigth = display_surf.get_height()
        self.background = None
        self.rect = Rect(0, 0, d_width, d_heigth)
        self.buttons = []
        self.input = None

    def on_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.rect.collidepoint(event.pos):
                    button.on_click(*button.args)
        elif event.type == KEYDOWN:
            if self.input is not None:
                self.input.on_text_changed(event.unicode)


class Login(Screen):
    def __init__(self, login):
        Screen.__init__(self)

        self.input = TextInput(52, [0, 0, 0], [0, 255, 0])
        self.input.rect.center = self.rect.center
        self.add(self.input)

        btn_login = Button('Enter', 42, [0, 0, 0], on_click=login)
        btn_login.rect.centerx = self.rect.centerx
        btn_login.rect.centery = int(self.rect.height * 0.60)
        self.background, _ = load_image('Brisca_Start.png')
        self.add(btn_login)
        self.buttons.append(btn_login)


class Lobby(Screen):
    def __init__(self, client):
        Screen.__init__(self)
        self.client = client
        self.background, _ = load_image('Brisca_Start.png')
        client.get_rooms(client.socket)
        self.available_rooms = UIList(
            [], 42, 315, self.join_room, Rect(0, 0, 640, 720))

        list_label = Label('Join Room:', 42, [255, 0, 0])
        list_label.rect.left = 200
        list_label.rect.centery = int(self.available_rooms.rect.height * 0.4)
        self.add(list_label)
        self.add(self.available_rooms)
        self.buttons.extend(self.available_rooms.items)

        create_label = Label('Create Room:', 42, [0, 0, 0])
        create_label.rect.right = 1080
        create_label.rect.centery = int(
            self.available_rooms.rect.height * 0.4)
        self.add(create_label)

        self.input = TextInput(42, [0, 0, 0], [255, 0, 0])
        self.input.rect.top = create_label.rect.bottom + 20
        self.input.rect.centerx = create_label.rect.centerx
        self.add(self.input)

        self.create_button = Button('Create', 42, [0, 0, 0], [
            0, 0, 255], self.create_room)
        self.create_button.rect.top = self.input.rect.bottom + 20
        self.create_button.rect.centerx = self.input.rect.centerx
        self.add(self.create_button)
        self.buttons.append(self.create_button)

    def create_room(self):
        self.client.create_room(self.client.socket, self.input.text)

    def join_room(self, room):
        self.client.join_room(self.client.socket, room)

    def update(self, *args):
        Screen.update(self, args)
        self.available_rooms.update((self.update_buttons))

    def update_buttons(self, new_list):
        self.buttons = []
        self.buttons.append(self.create_button)
        self.buttons.extend(new_list)

    def draw(self, surface):
        Screen.draw(self, surface)
        self.available_rooms.draw(surface)


class GamingBoard(Screen):
    def __init__(self, client):
        Screen.__init__(self)
        self.client = client
        self.background, _ = load_image('table.png')
        self.main_board = MainBoard()
        self.player_boards = (PlayerBoard(self.main_board.rect),
                              PlayerBoard(self.main_board.rect,
                                          PBoardSide.RIGHT),
                              PlayerBoard(self.main_board.rect,
                                          PBoardSide.TOP),
                              PlayerBoard(self.main_board.rect, PBoardSide.LEFT))
        self.add(self.main_board)
        self.add(self.player_boards)
        self.room = ''
        self.last_picked_index = 0

    def add_card(self, card, player, position=None):
        player_board = list(filter(lambda x: x.player ==
                                   player, self.player_boards))[0]
        rotation = None
        if player_board.board_position in (PBoardSide.LEFT, PBoardSide.RIGHT):
            rotation = 90
        card = Card(card, rotation)
        card.rect.center = self.main_board.deck.cards[3].rect.center
        if position is not None:
            card.target_pos = player_board.cards[position].rect.center
            self.player_boards[self.player_boards.index(
                player_board)].cards[position] = card
        else:
            card.target_pos = player_board.selected_card.rect.center
        self.add(card)

    def on_event(self, event):
        Screen.on_event(self, event)
        if event.type == MOUSEBUTTONDOWN:
            for index, card in enumerate(self.player_boards[0].cards):
                if card.rect.collidepoint(event.pos) and self.main_board.turn.text == self.client.username:
                    card.target_pos = self.player_boards[0].selected_card.rect.center
                    self.last_picked_index = index
                    self.client.card_pick(
                        self.client.socket, card.name, self.room)
                    return
