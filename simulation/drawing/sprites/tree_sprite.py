from glob import glob
import pygame
import random


class TreeSprite(pygame.sprite.Sprite):

    def __init__(self, image_store):
        super(TreeSprite, self).__init__()
        self.image_store = image_store
        self.image_index = 3
        self.index_appender = 0
        self.image_speed = 1
        self.fruit_tree = glob("assets/fruit_tree_*.svg")
        self.animation = [self.load_image(x) for x in self.fruit_tree]

    def load_image(self, filename):
        image = self.image_store.get(filename)
        if image is None:
            image = pygame.image.load(filename).convert_alpha()
            self.image_store.update({filename: image})
        return image

    def get_image(self, scale):
        # TODO: figure out a way to fix the svg issue without having to import and export with figma
        to_return = pygame.transform.scale(self.animation[self.image_index], (scale, scale))
        return to_return

    def notify(self, tree):
        self.image_index = tree.food_count

