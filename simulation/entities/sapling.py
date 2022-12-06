from drawing.sprites.sapling_sprite import SaplingSprite
from entities.entity_base import EntityBase
from entities.entity_enums import EntityType
from util.vector import Vector
from world.map.map_dto import MapDto
from world.time.tick_counter import TickCounter

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.tree import Tree



class Sapling(EntityBase):

    def __init__(self, position: Vector, tree_creator: 'Tree', data_collector=None):
        super().__init__(data_collector)
        self.grow_counter = TickCounter(320)
        self.position = position
        self.tree_creator = tree_creator
        self.sprite = None

    def tick(self, map_dto: MapDto):
        if self.grow_counter.tick():
            map_dto.get_entities(EntityType.TREE).append(self.tree_creator.create_tree())
            map_dto.get_entities(EntityType.SAPLING).remove(self)

    def get_input_value(self) -> int:
        return 1

    def get_sprite(self, sapling_painter):
        if self.sprite is None:
            self.sprite = SaplingSprite(sapling_painter.image_store)
        return self.sprite
