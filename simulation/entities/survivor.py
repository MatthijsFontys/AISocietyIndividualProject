import random
from ai.neuralnetwork import NeuralNetwork

from util.vector import Vector


class Survivor:

    def __init__(self, position):
        # movement
        self.position = position  # vector.Vector()
        self.velocity = Vector()

        self.speed = 2
        self.velocity_arr = [Vector(), Vector(0, -self.speed), Vector(0, self.speed), Vector(-self.speed, 0),
                             Vector(self.speed, 0)]

        # GeneticAlgorithm stuff
        self.brain = NeuralNetwork(6, 4).add_layer(8).add_layer(8).add_output_layer()

        self.fitness = 0
        self.fitness_increment = 1

        # stats
        self.fullness = 100

        # inventory (not used yet. it eats the food it finds immediately)
        self.food_count = 0
        self.food_limit = 2

    def increase_fitness(self):
        self.fitness += self.fitness_increment

    def decrease_fullness(self):
        self.fullness -= 0.5 # randint(0, 20)  # 10  # get depletion rate from dna  randint(0, 20)

    def is_dead(self):
        return self.fullness <= 0

    def give_food(self):
        # self.food_count = min(self.food_count + 1, self.food_limit)
        self.fullness += 20
        self.fullness = min(self.fullness, 100)

    def move(self, index):
        if not self.is_dead():
            # self.position.add(self.velocity)
            # self.position.add(random.choice(self.velocity_arr))
            self.position.add(self.velocity_arr[index])
