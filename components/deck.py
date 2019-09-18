from pygame.sprite import RenderPlain
from .card import Card


class Deck(RenderPlain):
    def __init__(self, parent_rect):
        RenderPlain.__init__(self)
        for i in range(0, 4):
            card = Card('back_red.png')
            card.rect.center = (100, 125)
            new_x = -int(card.rect.width / 2 - 16 + 4 * i)
            new_y = -int(card.rect.height / 2 - 16 + 4 * i)
            card.rect = card.rect.move(new_x, new_y)
            self.add(card)
