import pygame

from drawing.image_store import ImageStore
from util.draw_util import sprite_glob


class SaplingSprite(pygame.sprite.Sprite):

    def __init__(self, image_store):
        super(SaplingSprite, self).__init__()
        self.image_store: ImageStore = image_store
        self.paths = sprite_glob("sapling*.svg")
        self.images = [self.image_store.get(f) for f in self.paths]
        self.aspect_ratio = self.images[0].get_height() / self.images[0].get_width()

    def get_image(self, scale):
        return pygame.transform.scale(self.images[0], (scale, scale * self.aspect_ratio))
