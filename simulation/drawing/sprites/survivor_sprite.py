from glob import glob
import pygame


class SurvivorSprite(pygame.sprite.Sprite):

    def __init__(self, image_store):
        super(SurvivorSprite, self).__init__()
        self.image_store = image_store
        self.rotation = 0
        self.image_index = 0
        self.index_appender = 0
        self.image_speed = 20
        self.walk_animation = []
        self.walk_paths = glob("assets/survivor*.svg")
        self.walk_animation = [self.image_store.get(x) for x in self.walk_paths]

    def get_image(self, scale):
        to_return = pygame.transform.scale(self.walk_animation[self.image_index], (scale, scale))
        to_return = pygame.transform.rotate(to_return, self.rotation)
        return to_return

    def notify(self, index):
        # 0 - Idle, 1 - Up, 2 - Down, 3 - Left, 4 - Right
        if index > 0:
            self.rotation = (index - 1) * -45
            self.image_index = 0
        self.update()

    # override
    def update(self):
        self.index_appender += 1
        if self.index_appender == self.image_speed:
            self.image_index += 1
            self.index_appender = 0
        if self.image_index >= len(self.walk_animation):
            self.image_index = 0

