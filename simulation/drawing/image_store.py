import pygame


class ImageStore:

    def __init__(self):
        self.store = {}

    def get(self, filename):
        image = self.store.get(filename)
        if image is None:
            image = pygame.image.load(filename).convert_alpha()
            self.store.update({filename: image})
        return image
