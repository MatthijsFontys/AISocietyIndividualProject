from drawing.sprites.tree_sprite import TreeSprite
from entities.entity_base import EntityBase
from entities.entity_enums import EntityType
from entities.survivor import Survivor
from util.vector_pool import VectorPool
from world.data.data_enums import GlobalMetric
from world.map.map_dto import MapDto
from world.time.tick_counter import TickCounter

from entities.campfire import Campfire
from entities.sapling import Sapling


class Tree(EntityBase):

    def __init__(self, position, data_collector=None):
        super().__init__(data_collector)
        self.vector_pool = VectorPool()
        self.food_count = 3
        self.max_food_count = 3
        self.grow_counter = TickCounter(80)
        self.forage_counter = TickCounter(10)
        self.is_forageable = True
        self.did_ignite = False
        self.forage_range = 80
        self.ignite_range = 60
        self.forage_range_squared = self.forage_range ** 2
        self.ignite_range_squared = self.ignite_range ** 2
        self.position = position
        # transformations
        self.sapling = Sapling(self.position, self, self.data_collector)
        self.campfire = Campfire(self.position, self.sapling, self.data_collector)
        self.sprite = None

    def try_forage_food(self, survivor: Survivor) -> bool:
        is_in_range = self.position.get_distance_squared(survivor.position,
                                                         self.vector_pool.lend()) <= self.forage_range_squared
        if self.food_count > 0 and is_in_range and self.is_forageable:
            self.update_food_count(-1)
            survivor.give_food()
            self.forage_counter.reset()
            self.is_forageable = False
            self.data_collector.add_data(GlobalMetric.BERRIES_FORAGED)
            return True
        return False

    def try_ignite(self, survivor: Survivor, map_dto: MapDto):
        can_ignite = self.position.get_distance_squared(survivor.position,
                                                        self.vector_pool.lend()) <= self.ignite_range_squared
        if can_ignite and not self.did_ignite:
            self.did_ignite = True
            self.data_collector.add_data(GlobalMetric.TREES_IGNITED)
            map_dto.get_entities(EntityType.CAMPFIRE).append(self.campfire)
            map_dto.get_entities(EntityType.TREE).remove(self)
        return can_ignite

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

    def get_input_value(self) -> int:
        return self.food_count + 1

    def create_tree(self):
        return Tree(self.position, self.data_collector)

    def update_food_count(self, delta_food):
        self.food_count += delta_food
        if self.sprite is not None:
            self.sprite.notify(self)
