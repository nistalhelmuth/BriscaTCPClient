import pygame.display as display
import pygame.transform as transform
from enum import Enum
from pygame import Rect
from pygame.sprite import RenderPlain
from .card import Card
from .deck import Deck
from .ui import Label
from utils.loaders import load_image


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
        self.triunf = Card('empty.png', 90, -1)
        self.triunf.rect.center = self.deck.cards[0].rect.center
        self.triunf.rect = self.triunf.rect.move(50, 0)
        self.add(self.triunf)
        self.add(self.deck)

        turn_label = Label('Turn:', 22, [0, 0, 0])
        turn_label.rect.right = 1180
        self.add(turn_label)
        self.turn = Label('', 22, [0, 0, 0])
        self.turn.rect.top = turn_label.rect.bottom
        self.turn.rect.centerx = turn_label.rect.centerx
        self.add(self.turn)

    def update_triunf(self, card):
        self.triunf.image, _ = load_image(card + '.png')
        self.triunf.image = transform.rotate(self.triunf.image, 90)


class PlayerBoard(RenderPlain):
    def __init__(self, main_board_rect, board_position=PBoardSide.BOTTOM):
        RenderPlain.__init__(self)
        self.board_position = board_position
        self.can_play = False
        self.player = '(Empty)'

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

        self.label = Label(self.player, 20, [0, 0, 0])
        self.label.rect.centerx = self.rect.centerx
        if board_position == PBoardSide.BOTTOM:
            self.label.rect.bottom = self.rect.bottom - 5
        elif board_position == PBoardSide.TOP:
            self.label.rect.bottom = self.rect.top + 20
        else:
            self.label.rect.bottom = self.rect.top - 30
        self.add(self.label)

        self.cards = []
        for i in range(-1, 2):
            card = None
            if self.board_position == PBoardSide.BOTTOM:
                card = Card('empty.png', card_rotation, -1)
            else:
                card = Card('back_red.png', card_rotation)

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

        self.selected_card = Card('empty.png', card_rotation, -1)
        self.winns = Card('empty.png', card_rotation, -1)
        if board_position == PBoardSide.BOTTOM:
            self.selected_card.rect.centerx = main_board_rect.centerx
            self.selected_card.rect.bottom = main_board_rect.bottom - 5
            self.winns.rect.centery = self.rect.centery + 30
            self.winns.rect.left = self.rect.right + 20
        elif board_position == PBoardSide.TOP:
            self.selected_card.rect.centerx = main_board_rect.centerx
            self.selected_card.rect.top = main_board_rect.top + 5
            self.winns.rect.centery = self.rect.centery - 30
            self.winns.rect.right = self.rect.left - 20
        elif board_position == PBoardSide.LEFT:
            self.selected_card.rect.centery = main_board_rect.centery
            self.selected_card.rect.left = main_board_rect.left + 5
            self.winns.rect.centerx = self.rect.centerx - 30
            self.winns.rect.top = self.rect.bottom + 60
        elif board_position == PBoardSide.RIGHT:
            self.selected_card.rect.centery = main_board_rect.centery
            self.selected_card.rect.right = main_board_rect.right - 5
            self.winns.rect.centerx = self.rect.centerx + 30
            self.winns.rect.bottom = self.rect.top - 60
        self.add(self.selected_card)
        self.add(self.winns)
