from random import randrange

from entities.entity_enums import EntityType
from entities.survivor import Survivor
from map_creator.map_save import MapSave
from entities.tree import Tree
from util.vector import Vector


class WorldMap:

    def __init__(self, save: MapSave, population_size):
        self.WIDTH = save.width
        self.HEIGHT = save.height
        self.POPULATION_SIZE = population_size

        # Might map below from save in future
        self.time_perception = -1
        self.spawn_points = []
        # Entities
        self.population = [Survivor(Vector(randrange(self.WIDTH), randrange(self.HEIGHT))) for _ in range(population_size)]
        self.saplings = []
        self.campfires = []
        self.trees = [Tree(tree_pos) for tree_pos in save.entities.get(EntityType.TREE.name)]

