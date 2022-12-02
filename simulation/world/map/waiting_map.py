import random

from ai.my_neat import MyNeat
from entities.survivor import Survivor
from map_creator.map_save import MapSave
from world.map.world_base import WorldBase
from functools import reduce


class WaitingMap(WorldBase):

    def __init__(self, save: MapSave, population_size, cell_size, neat: MyNeat):
        super().__init__(save, population_size, cell_size)
        self.generation = self.population.copy()
        self.neat = neat

    def repopulate(self, genomes):
        for _, genome in genomes:
            self.population.append(Survivor(self.get_rand_position(), genome, self.neat.create_brain(genome), self.data_collector))
        self.generation = self.population.copy()

    def dequeue(self, birthday: int):
        offspring = None
        if len(self.population) > 0:
            offspring = self.population.pop()
            offspring.birthday = birthday
        elif self.generation:
            genome = self.pick_parent().create_mutated_genome(self.neat.CONFIG.genome_config)
            offspring = Survivor(self.get_rand_position(), genome, self.neat.create_brain(genome))

        return offspring

    def get_percent_alive(self):
        return reduce(lambda x, y: x + (0 if y.is_dead() else 1), self.generation, 0) / self.POPULATION_SIZE

    def pick_parent(self):
        rand = random.random()
        summed_score = reduce(lambda accumulator, element: accumulator + element.genome.fitness, self.generation, 0)
        for member in self.generation:
            rand -= member.genome.fitness / summed_score
            if rand <= 0:
                return member
        if not self.generation:
            return None
        print('No parent found!')
        return random.choice(self.generation)
