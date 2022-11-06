from ai.my_neat import MyNeat
from entities.survivor import Survivor
from map_creator.map_save import MapSave
from world.world_map import WorldMap
from functools import reduce


class WaitingMap(WorldMap):

    def __init__(self, save: MapSave, population_size, cell_size):
        super().__init__(save, population_size, cell_size)
        self.generation = self.population.copy()

    def repopulate(self, genomes, neat: MyNeat):
        for _, genome in genomes:
            self.population.append(Survivor(self.get_rand_position(), genome, neat.create_brain(genome)))
        self.generation = self.population.copy()

    def dequeue(self, birthday: int):
        if len(self.population) > 0:
            offspring = self.population.pop()
            offspring.birthday = birthday
            return offspring
        return None

    def get_percent_alive(self):
        return reduce(lambda x, y: x + (0 if y.is_dead() else 1), self.generation, 0) / self.POPULATION_SIZE
