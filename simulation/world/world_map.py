from random import randrange

from entities.entity_enums import EntityType
from entities.survivor import Survivor
from map_creator.map_save import MapSave
from entities.tree import Tree
from util.vector import Vector
from world.collision_grid import CollisionGrid
from world.map_dto import MapDto


class WorldMap:

    def __init__(self, save: MapSave, population_size, cell_size):
        self.WIDTH = save.width
        self.HEIGHT = save.height
        self.POPULATION_SIZE = population_size

        # Might map below from save in future
        self.time_perception = -1
        self.spawn_points = []
        # Entities
        self.population = []
        self.saplings = []
        self.campfires = []

        self.trees = [Tree(tree_pos) for tree_pos in save.get_entities(EntityType.TREE)]
        self.dto = MapDto(
                               self.trees, self.population, self.saplings, self.campfires,
                               self.HEIGHT, self.WIDTH, self.POPULATION_SIZE
                               )
        self.collision_grid = CollisionGrid(cell_size, self.dto)
        self.entities = {
            EntityType.TREE.name: self.trees,
            EntityType.SAPLING.name: self.saplings,
            EntityType.CAMPFIRE.name: self.campfires,
            EntityType.SURVIVOR.name: self.population
        }

    def get_entities(self, t: EntityType):
        return self.entities.get(t.name)

    def get_rand_position(self, to_set: Vector = None):
        return Vector.unpack_nullable(randrange(self.WIDTH), randrange(self.HEIGHT), to_set)

