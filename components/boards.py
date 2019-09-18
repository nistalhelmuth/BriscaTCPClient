import pygame.display as display
from enum import Enum
from pygame import Rect
from pygame.sprite import RenderPlain
from .card import Card
from .deck import Deck


class PBoardSide(Enum):
    BOTTOM = 0
    RIGHT = 1
    TOP = 2
    LEFT = 3


BOARD_ROTATIONS = {
    PBoardSide.BOTTOM: 0,
    PBoardSide.RIGHT: 90,
    PBoardSide.TOP: 180,
    PBoardSide.LEFT: 270,
}


class BoardRef():
    def __init__(self, left, top):
        self.left = left
        self.top = top


BOARD_REFERENCES = {
    PBoardSide.BOTTOM: BoardRef('left', 'bottom'),
    PBoardSide.RIGHT: BoardRef('right', 'top'),
    PBoardSide.TOP: BoardRef('left', 0),
    PBoardSide.LEFT: BoardRef(0, 'top'),
}


class MainBoard(RenderPlain):
    def __init__(self):
        RenderPlain.__init__(self)
        display_surf = display.get_surface()
        d_width = display_surf.get_width()
        d_heigth = display_surf.get_height()
        self.rect = Rect(int(0.3 * d_width), int(0.3 * d_heigth),
                         int(0.4 * d_width), int(0.4 * d_heigth))
        self.deck = Deck(self.rect)
        self.add(self.deck)


class PlayerBoard(RenderPlain):
    def __init__(self, main_board_rect, board_position=PBoardSide.BOTTOM):
        RenderPlain.__init__(self)
        self.board_position = board_position

        display_surf = display.get_surface()
        d_width = display_surf.get_width()
        d_heigth = display_surf.get_height()

        w_ratio, h_ratio = (0.4, 0.3)
        card_rotation = None
        if board_position in (PBoardSide.LEFT, PBoardSide.RIGHT):
            w_ratio, h_ratio = h_ratio, w_ratio
            card_rotation = 90
        width = int(d_width * w_ratio)
        height = int(d_heigth * h_ratio)

        left = top = None
        board_ref = BOARD_REFERENCES[board_position]
        if isinstance(board_ref.left, str):
            left = getattr(main_board_rect, board_ref.left)
        else:
            left = main_board_rect.left - width
        if isinstance(board_ref.top, str):
            top = getattr(main_board_rect, board_ref.top)
        else:
            top = board_ref.top

        self.rect = Rect(left, top, width, height)

        self.cards = []
        for i in range(-1, 2):
            card = Card('clubs_1.png', card_rotation)
            if board_position in (PBoardSide.LEFT, PBoardSide.RIGHT):
                card.rect.centerx = self.rect.centerx
                card.rect.centery = int(
                    self.rect.centery + self.rect.height * 0.25 * i + i * 50)
            else:
                card.rect.centery = self.rect.centery
                card.rect.centerx = int(
                    self.rect.centerx + self.rect.width * 0.25 * i)
            self.add(card)
            self.cards.append(card)

        self.selected_card = Card('empty.png', card_rotation)
        self.selected_card.rect.center = (self.rect.centerx, self.rect.top)
        self.add(self.selected_card)
