from drawing.sprites.entity_sprite_base import EntitySpriteBase


class TreeSprite(EntitySpriteBase):

    def __init__(self, image_store):
        super(TreeSprite, self).__init__(image_store, "fruit_tree_*.svg")

    def notify(self, tree):
        self.image_index = tree.food_count

