from glob import glob
import pygame
import random


class SurvivorSprite(pygame.sprite.Sprite):

    def __init__(self):
        super(SurvivorSprite, self).__init__()
        self.rotation = random.randint(0, 4) * 90
        self.image_index = 0
        self.index_appender = 0
        self.image_speed = 20
        self.walk_animation = []
        self.walk_paths = glob("assets/survivor*.svg")
        self.load_images()

    def load_image(self, filename):
        return pygame.image.load(filename).convert_alpha()

    def load_images(self):
        self.walk_animation = [self.load_image(x) for x in self.walk_paths]

    # TODO: Might need to create a cache for the scaled images if it becomes slow
    def get_image(self, scale):
        to_return = pygame.transform.scale(self.walk_animation[self.image_index], (scale, scale))
        to_return = pygame.transform.rotate(to_return, self.rotation)
        return to_return

    # override
    def update(self):
        self.index_appender += 1
        if self.index_appender == self.image_speed:
            self.image_index += 1
            self.index_appender = 0
        # self.rotation += 90
        # self.rotation = self.rotation % 360
        if self.image_index >= len(self.walk_animation):
            self.image_index = 0

