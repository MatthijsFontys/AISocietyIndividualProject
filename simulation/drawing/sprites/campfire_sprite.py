import pygame

from drawing.image_store import ImageStore
from util.draw_util import sprite_glob


class CampfireSprite(pygame.sprite.Sprite):

    def __init__(self, image_store):
        super(CampfireSprite, self).__init__()
        self.image_store: ImageStore = image_store
        self.paths = sprite_glob("campfire*.svg")
        self.images = [self.image_store.get(f) for f in self.paths]

    def get_image(self, scale):
        return pygame.transform.scale(self.images[0], (scale, scale))





