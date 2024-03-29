import copy
import neat
import numpy as np
from drawing.sprites.survivor_sprite import SurvivorSprite
from entities.entity_base import EntityBase
from util.vector import Vector
from world.map.map_dto import MapDto
from world.data.data_collector import DataCollector
from world.data.data_enums import GlobalMetric


class Survivor(EntityBase):

    def __init__(self, position, genome, brain, data_collector=None, birthday=0):
        # movement
        super().__init__(data_collector)
        self.position = position

        self.speed = 4
        self.velocity_arr = [Vector(), Vector(0, -self.speed), Vector(self.speed / 2, -self.speed / 2),
                             Vector(self.speed, 0), Vector(self.speed / 2, self.speed / 2), Vector(0, self.speed),
                             Vector(-self.speed / 2, self.speed / 2), Vector(-self.speed, 0),
                             Vector(-self.speed / 2, -self.speed / 2)
                             ]

        # GeneticAlgorithm stuff
        self.brain = brain
        self.genome = genome
        self.genome.fitness = 0

        # stats
        self.fullness = 100
        self.temperature = 100
        # drawing
        self.sprite = None
        self.birthday = birthday

    def tick(self, map_dto: MapDto):
        self.genome.fitness += 1
        self.fullness -= map_dto.get_hunger_loss()
        self.temperature -= map_dto.get_temperature_loss()
        if self.is_dead():
            map_dto.population.remove(self)
            self.data_collector.add_data(GlobalMetric.DEATHS)

    """
    Make it so that when agents transferred to the overworld, that their stats get refilled,
    but get their score lowered, to better reflect being born in the visible world
    """

    def get_input_value(self) -> int:
        return 0

    def start_exist(self, data_collector: DataCollector):
        self.data_collector = data_collector
        self.genome.fitness -= 100 - self.fullness
        self.genome.fitness -= 100 - self.temperature
        self.genome.fitness = max(self.genome.fitness, 0)
        self.temperature = 100
        self.fullness = 100

    def is_dead(self):
        if self.temperature <= 0:
            self.data_collector.add_data(GlobalMetric.DEATHS_BY_HYPOTHERMIA)
            return True

        if self.fullness <= 0:
            self.data_collector.add_data(GlobalMetric.DEATHS_BY_STARVATION)
            return True

        return False

    def give_food(self):
        self.fullness += 20
        self.fullness = min(self.fullness, 100)

    def move(self, index, world: MapDto):
        if not self.is_dead():
            self.position.add(self.velocity_arr[index])
            self.position.x = np.clip(self.position.x, 0, world.WIDTH - 50)
            self.position.y = np.clip(self.position.y, 0, world.HEIGHT - 50)
            if self.sprite is not None:
                self.sprite.notify(index)

    def init_sprite(self, survivor_painter):
        return SurvivorSprite(survivor_painter.image_store)

    def create_mutated_genome(self, neat_config) -> neat.genome.DefaultGenome:
        mutated_genes: neat.genome.DefaultGenome = copy.deepcopy(self.genome)
        mutated_genes.fitness = 0
        mutated_genes.mutate(neat_config)
        return mutated_genes

