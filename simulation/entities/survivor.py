import random
from ai.neuralnetwork import NeuralNetwork
from drawing.sprites.survivor_sprite import SurvivorSprite

from util.vector import Vector
from world.map_dto import MapDto


class Survivor:

    def __init__(self, position):
        # movement
        self.position = position  # vector.Vector()

        self.speed = 2
        self.velocity_arr = [Vector(), Vector(0, -self.speed), Vector(-self.speed, 0), Vector(0, self.speed),
                             Vector(self.speed, 0)]

        # GeneticAlgorithm stuff
        self.brain = NeuralNetwork(6, 4).add_layer(8).add_layer(8).build()
        self.genome = None
        self.fitness = 0

        # stats
        self.fullness = 100
        self.temperature = 100
        # drawing
        self.sprite = None

    def tick(self, map_dto: MapDto):
        #self.genome.fitness += 1
        self.fullness -= 0.5
        self.temperature -= 0.2
        if self.is_dead():
            map_dto.population.remove(self)

    def is_dead(self):
        return self.fullness <= 0

    def give_food(self):
        self.fullness += 20
        self.fullness = min(self.fullness, 100)

    def move(self, index):
        if not self.is_dead():
            self.position.add(self.velocity_arr[index])
            if self.sprite is not None:
                self.sprite.notify(index)

    def get_sprite(self, survivor_painter):
        if self.sprite is None:
            self.sprite = SurvivorSprite(survivor_painter.image_store)
        return self.sprite
