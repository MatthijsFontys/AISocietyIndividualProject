from map_creator.map_save import MapSave
from world.world_map import WorldMap
from functools import reduce


class WaitingMap(WorldMap):

    def __init__(self, save: MapSave, population_size, cell_size):
        super().__init__(save, population_size, cell_size)
        self.generation = self.population.copy()

    def repopulate(self, genomes):
        self.generation = self.population.copy()

    def dequeue(self):
        if len(self.population) > 0:
            return self.population.pop()
        return None

    def get_percent_alive(self):
        reduce(lambda x, y: x + 1 if y.isAlive() else 0, self.generation) / len(self.generation)
