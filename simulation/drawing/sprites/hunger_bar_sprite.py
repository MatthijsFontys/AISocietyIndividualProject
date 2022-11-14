from drawing.sprites.stat_bar_base import StatBarBase
from world.map.map_dto import MapDto


class HungerBarSprite(StatBarBase):

    def __init__(self, image_store, width):
        super().__init__(image_store, width, 'hunger_bar*.svg')
