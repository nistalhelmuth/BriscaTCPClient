import os
from pygame.sprite import Sprite, Rect
from pygame.font import Font

FONT = os.path.join('assets', 'upheavtt.ttf')


class Label(Sprite):
    def __init__(self, text, size, text_color, background_color=None):
        Sprite.__init__(self)
        self.text = text
        self.image = Font(FONT, size).render(
            text, True, text_color, background_color)
        self.rect = self.image.get_rect()


class Button(Label):
    def __init__(self, text, size, text_color, background_color=None, on_click=None, args=()):
        Label.__init__(self, text, size, text_color, background_color)
        self.on_click = on_click
        self.args = args


class TextInput(Label):
    def __init__(self, size, text_color, background_color):
        Label.__init__(self, '', size, text_color, background_color)
        self.size = size
        self.text_color = text_color
        self.background_color = background_color

    def on_text_changed(self, newText):
        self.text += newText
        self.image = Font(FONT, self.size).render(
            self.text, True, self.text_color, self.background_color)
        previous_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = previous_center
