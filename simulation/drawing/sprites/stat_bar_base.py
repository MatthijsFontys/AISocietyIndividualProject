from drawing.image_store import ImageStore
from util.draw_util import sprite_glob
import pygame.sprite
import pygame
from util.linalg import lerp


class StatBarBase(pygame.sprite.Sprite):

    def __init__(self, image_store, width, glob_pattern, prefix):
        super(StatBarBase, self).__init__()
        self.prefix = prefix
        self.drawn_value = 100
        self.value = self.drawn_value
        self.image_store: ImageStore = image_store
        self.images = [self.image_store.get(x) for x in sprite_glob(glob_pattern)]
        self.aspect_ratio = self.images[0].get_width() / self.images[0].get_height()
        self.width = width
        self.height = self.width / self.aspect_ratio
        self.size = (self.width, (self.width / self.aspect_ratio))
        self.image_store.deposit(f'{self.prefix}_outline', pygame.transform.smoothscale(self.images[1], self.size))

    def get_image(self, value):
        if abs(value - self.value) > 5 or value == 100 or value == 0:
            self.value = value

        self.drawn_value = lerp(self.drawn_value, self.value, 0.2)
        fill = pygame.transform.scale(self.images[0], self.size)
        canvas = pygame.Surface(self.size).convert_alpha()
        canvas.fill(pygame.Color(0, 0, 0, 0))
        canvas.blit(fill, (0, 0), area=(0, 0, self.width * (self.drawn_value / 100), fill.get_height()))
        canvas.blit(self.image_store.get(f'{self.prefix}_outline'), (0, 0))
        return canvas
