from drawing.sprites.entity_sprite_base import EntitySpriteBase
from entities.entity_base import EntityBase
from entities.entity_enums import EntityType
from entities.sapling import Sapling
from entities.survivor import Survivor
from util.vector import Vector
from util.vector_pool import VectorPool
from world.map.map_dto import MapDto
from world.time.tick_counter import TickCounter


class Campfire(EntityBase):

    def __init__(self, position: Vector, sapling: Sapling, data_collector=None):
        super().__init__(data_collector)
        self.vector_pool = VectorPool()
        self.sapling = sapling
        self.heat = 1
        self.heat_range = 100
        self.heat_range_squared = self.heat_range ** 2
        self.fuel_counter = TickCounter(500)
        self.position = position

    def tick(self, map_dto: MapDto):
        if self.fuel_counter.tick():
            map_dto.get_entities(EntityType.SAPLING).append(self.sapling)
            map_dto.get_entities(EntityType.CAMPFIRE).remove(self)

    def try_give_warmth(self, survivor: Survivor) -> bool:
        is_in_range = self.position.get_distance_squared(survivor.position,
                                                         self.vector_pool.lend()) <= self.heat_range_squared
        if is_in_range:
            survivor.temperature = min(100, survivor.temperature + self.heat)
        return is_in_range

    def get_input_value(self) -> int:
        return 5

    def init_sprite(self, campfire_painter):
        return EntitySpriteBase(campfire_painter.image_store, "campfire*.svg", rand_rotate=True)
