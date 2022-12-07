import pygame

from drawing.sprites.entity_sprite_base import EntitySpriteBase


class SurvivorSprite(EntitySpriteBase):

    def __init__(self, image_store):
        super(SurvivorSprite, self).__init__(image_store, "survivor*.svg")

    def notify(self, index):
        # 0 - Idle, 1 - Up, 2 - Down, 3 - Left, 4 - Right
        if index > 0:
            self.rotation = (index - 1) * -45
            self.image_index = 0
