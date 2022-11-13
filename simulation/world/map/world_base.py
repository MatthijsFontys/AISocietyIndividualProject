from abc import ABC
from random import randrange
from entities.entity_enums import EntityType
from map_creator.map_save import MapSave
from entities.tree import Tree
from util.vector import Vector
from world.map.collision_grid import CollisionGrid
from world.map.map_dto import MapDto


class WorldBase(ABC):

    def __init__(self, save: MapSave, population_size, cell_size):
        self.WIDTH = save.width
        self.HEIGHT = save.height
        self.POPULATION_SIZE = population_size

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
        self.fullness_loss = 0.5
        self.temperature_loss = 0  # 0.2
        self.dto = MapDto(
            self.entities, self.trees, self.population, self.saplings, self.campfires,
            self.HEIGHT, self.WIDTH, self.POPULATION_SIZE,
            self.fullness_loss, self.temperature_loss
        )
        self.collision_grid = CollisionGrid(cell_size, self.dto)

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
