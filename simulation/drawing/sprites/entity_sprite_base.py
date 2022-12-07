import pygame
from random import randint
from drawing.image_store import ImageStore
from util.draw_util import sprite_glob


class EntitySpriteBase(pygame.sprite.Sprite):

    def __init__(self, image_store: ImageStore, glob_pattern: str, rand_rotate=False, aspect_index=0):
        super(EntitySpriteBase, self).__init__()
        self.image_index = 0
        self.image_store: ImageStore = image_store
        self.paths = sprite_glob(glob_pattern)
        self.images = [self.image_store.get(f) for f in self.paths]
        self.aspect_ratio = self.images[aspect_index].get_height() / self.images[aspect_index].get_width()
        self.rotation = randint(0, 360) if rand_rotate else 0

    def get_image(self, scale):
        img = pygame.transform.scale(self.images[self.image_index], (scale, scale * self.aspect_ratio))
        img = pygame.transform.rotate(img, self.rotation)
        return img
