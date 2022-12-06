from abc import ABC
from random import randrange
from entities.entity_enums import EntityType
from map_creator.map_save import MapSave
from entities.tree import Tree
from util.vector import Vector
from world.map.collision_grid import CollisionGrid
from world.map.map_dto import MapDto
from world.time.game_tick_dto import GameTickDto
from util.linalg import lerp


class WorldBase(ABC):

    def __init__(self, save: MapSave, population_size, cell_size, tick_dto: GameTickDto):
        self.WIDTH = save.width
        self.HEIGHT = save.height
        self.POPULATION_SIZE = population_size

        self.tick_dto = tick_dto
        self.data_collector = None
        # Might map below from save in future
        self.time_perception = -1
        self.spawn_points = []
        # Entities
        self.population = []
        self.saplings = []
        self.campfires = []

        self.trees = [Tree(tree_pos) for tree_pos in save.get_entities(EntityType.TREE)]
        self.entities = {
            EntityType.TREE.name: self.trees,
            EntityType.SAPLING.name: self.saplings,
            EntityType.CAMPFIRE.name: self.campfires,
            EntityType.SURVIVOR.name: self.population
        }
        # 0 - hunger | 1 = temperature  is pass as array for reference type benefits
        self.stat_loss = [0.5, 0.25]
        self.dto = MapDto(
            self.entities, self.trees, self.population, self.saplings, self.campfires,
            self.HEIGHT, self.WIDTH, self.POPULATION_SIZE,
            self.stat_loss
        )
        self.collision_grid = CollisionGrid(cell_size, self.dto)

    def tick(self, _: bool):
        day_percent = self.tick_dto.get_day_percent()
        if day_percent < 0.5:
            self.stat_loss[1] = lerp(0.75, 0.25, day_percent)
        else:
            self.stat_loss[1] = lerp(0.25, 0.75, (day_percent-0.5) / 0.5)

    def set_data_collector(self, data_collector):
        if self.data_collector is None:
            self.data_collector = data_collector
        self.for_each_entity(lambda x: x.set_data_collector(self.data_collector))

    def for_each_entity(self, func):
        for t in EntityType:
            for entity in reversed(self.get_entities(t)):
                func(entity)

    def get_entities(self, t: EntityType):
        return self.entities.get(t.name)

    def get_rand_position(self, to_set: Vector = None):
        return Vector.unpack_nullable(randrange(self.WIDTH), randrange(self.HEIGHT), to_set)
