from util.draw_util import sprite_glob
import pygame.sprite
from util.linalg import lerp


class StatBarBase(pygame.sprite.Sprite):

    def __init__(self, image_store, width, glob_pattern):
        super(StatBarBase, self).__init__()
        self.drawn_value = 100
        self.value = self.drawn_value
        self.image_store = image_store
        self.images = [self.image_store.get(x) for x in sprite_glob(glob_pattern)]
        self.aspect_ratio = self.images[0].get_width() / self.images[0].get_height()
        self.width = width * 0.75
        self.height = self.width / self.aspect_ratio

    def get_image(self, value):
        if abs(value - self.value) > 5 or value == 100 or value == 0:
            self.value = value

        self.drawn_value = lerp(self.drawn_value, self.value, 0.2)
        size = (self.width, (self.width / self.aspect_ratio))
        fill = pygame.transform.scale(self.images[0], size)
        outline = pygame.transform.scale(self.images[1], size)
        canvas = pygame.Surface(size).convert_alpha()
        canvas.fill(pygame.Color(0, 0, 0, 0))
        canvas.blit(fill, (0, 0), area=(0, 0, self.width * (self.drawn_value / 100), fill.get_height()))
        canvas.blit(outline, (0, 0))
        return canvas
