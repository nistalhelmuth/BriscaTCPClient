import os
from pygame.sprite import Sprite, Rect, RenderPlain
from pygame.font import Font

FONT = os.path.join('assets', 'upheavtt.ttf')


class Label(Sprite):
    def __init__(self, text, size, text_color, background_color=None):
        Sprite.__init__(self)
        self.text = text
        self.previous_text = text
        self.size = size
        self.text_color = text_color
        self.background_color = background_color
        self.image = Font(FONT, size).render(
            text, True, text_color, background_color)
        self.rect = self.image.get_rect()

    def update(self, *args):
        if self.previous_text != self.text:
            self.image = Font(FONT, self.size).render(
                self.text, True, self.text_color, self.background_color)
            previous_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = previous_center
            self.previous_text = self.text


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


class UIList(RenderPlain):
    def __init__(self, data_list, item_size, starting_y, on_item_clicked=None, rect=None):
        RenderPlain.__init__(self)
        self.list = data_list
        self.last_count = 0
        self.on_item_clicked = on_item_clicked
        self.items = []
        self.item_size = item_size
        self.starting_y = starting_y
        self.rect = rect
        self.update()

    def update(self, *args):
        if len(self.list) != self.last_count:
            self.empty()
            self.items = []
            for index, item in enumerate(self.list):
                button = Button(item, self.item_size, [0, 0, 0],
                                on_click=self.on_item_clicked, args=(item,))
                self.add(button)
                button.rect.centerx = self.rect.centerx
                button.rect.top = self.starting_y + self.item_size * index + 10
                self.items.append(button)
            self.last_count = len(self.list)
            args[0](self.items)

    def draw(self, surface):
        RenderPlain.draw(self, surface)

    def update_list(self, new_list):
        self.list = new_list
