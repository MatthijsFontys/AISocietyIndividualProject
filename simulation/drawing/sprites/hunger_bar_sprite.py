from drawing.sprites.stat_bar_base import StatBarBase


class HungerBarSprite(StatBarBase):

    def __init__(self, image_store, width):
        super().__init__(image_store, width, 'assets/hunger_bar*.svg')
