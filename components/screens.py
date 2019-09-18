import pygame.display as display
from pygame import MOUSEBUTTONDOWN, KEYDOWN
from pygame.sprite import RenderPlain, Rect
from utils.loaders import load_image
from .boards import MainBoard, PlayerBoard, PBoardSide
from .ui import Button, Label, TextInput


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
    def __init__(self, on_login):
        Screen.__init__(self)

        self.input = TextInput(52, [0, 0, 0], [0, 255, 0])
        self.input.rect.center = self.rect.center
        self.add(self.input)

        btn_login = Button('Enter', 42, [0, 0, 0], on_click=on_login)
        btn_login.rect.centerx = self.rect.centerx
        btn_login.rect.centery = int(self.rect.height * 0.60)
        self.background, _ = load_image('Brisca_Start.png')
        self.add(btn_login)
        self.buttons.append(btn_login)


class GamingBoard(Screen):
    def __init__(self):
        Screen.__init__(self)
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

    def on_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            for card in self.player_boards[0].cards:
                if card.rect.collidepoint(event.pos):
                    card.target_pos = self.player_boards[0].selected_card.rect.center
                    return
