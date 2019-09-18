"""
Useful functions to load assets.
"""
import os
from pygame.image import load
from pygame import error, RLEACCEL


def load_image(name, colorkey=None):
    """
    Loads an image. This function was taken from the Line By Line Chimp
    tutorial at https://www.pygame.org/docs/tut/ChimpLineByLine.html.
    """
    fullname = os.path.join('assets', name)
    try:
        image = load(fullname)
    except error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()
