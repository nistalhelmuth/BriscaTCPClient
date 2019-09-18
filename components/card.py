import pygame.transform as transform
from pygame.sprite import Sprite
from utils.loaders import load_image


class Card(Sprite):
    """
    Class that represents a card.
    """

    def __init__(self, card_name, rotation=None, colorkey=None):
        Sprite.__init__(self)
        self.image, self.rect = load_image(card_name, colorkey)
        if rotation is not None:
            self.image = transform.rotate(self.image, rotation)
        self.rect = self.image.get_rect()
        self.target_pos = None
        print()

    def update(self, *args):
        if self.target_pos is None:
            return

        speed = 30
        dir_x, dir_y = (1, 1)
        if self.target_pos[0] < self.rect.centerx:
            dir_x = -1
        if self.target_pos[1] < self.rect.centery:
            dir_y = -1
        if (self.rect.centerx < self.target_pos[0] - speed or
            self.rect.centerx > self.target_pos[0] + speed or
            self.rect.centery < self.target_pos[1] - speed or
                self.rect.centery > self.target_pos[1] + speed):
            self.rect.move_ip(dir_x * speed, dir_y * speed)
