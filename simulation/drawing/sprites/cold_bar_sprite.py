from drawing.sprites.stat_bar_base import StatBarBase


class ColdBarSprite(StatBarBase):

    def __init__(self, image_store, width):
        super().__init__(image_store, width, 'drawing/assets/images/cold_bar*.svg')


