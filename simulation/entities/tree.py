from drawing.sprites.tree_sprite import TreeSprite
from entities.entity_base import EntityBase
from util.vector_pool import VectorPool
from world.data.data_enums import GlobalMetric
from world.map.map_dto import MapDto
from world.time.tick_counter import TickCounter


class Tree(EntityBase):

    def __init__(self, position, data_collector=None):
        super().__init__(data_collector)
        self.vector_pool = VectorPool()
        self.food_count = 3
        self.max_food_count = 3
        self.grow_counter = TickCounter(80)
        self.forage_counter = TickCounter(10)
        self.is_forageable = True
        self.forage_range = 80
        self.forage_range_squared = self.forage_range ** 2
        self.position = position
        self.sprite = None

    def try_forage_food(self, survivor) -> bool:
        is_in_range = self.position.get_distance_squared(survivor.position, self.vector_pool.lend()) <= self.forage_range_squared
        if self.food_count > 0 and is_in_range and self.is_forageable:
            self.update_food_count(-1)
            survivor.give_food()
            self.forage_counter.reset()
            self.is_forageable = False
            self.data_collector.add_data(GlobalMetric.BERRIES_FORAGED)
            return True
        return False

    def tick(self, _: MapDto):
        if self.grow_counter.tick() and self.food_count < self.max_food_count:
            self.update_food_count(1)
            self.data_collector.add_data(GlobalMetric.BERRIES_GROWN)
        if self.forage_counter.tick():
            self.is_forageable = True

    def get_sprite(self, tree_painter):
        if self.sprite is None:
            self.sprite = TreeSprite(tree_painter.image_store)
        return self.sprite

    def update_food_count(self, delta_food):
        self.food_count += delta_food
        if self.sprite is not None:
            self.sprite.notify(self)

