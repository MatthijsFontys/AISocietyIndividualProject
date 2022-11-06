import pygame.sprite


class ColdBarSprite(pygame.sprite.Sprite):

    def __init__(self, image_store):
        super(ColdBarSprite, self).__init__()
        self.image_store = image_store
        self.value = 100
        self.images = ("assets/survivor*.svg")

