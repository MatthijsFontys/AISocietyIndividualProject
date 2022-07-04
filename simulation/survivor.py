import random

from vector import Vector
from random import randint, choice


class Survivor:

    def __init__(self, position):

        # movement
        self.position = position  # vector.Vector()
        self.velocity = Vector()

        # TODO: REMOVE AFTER TESTING IS DONE
        self.speed = 2
        #self.velocity_arr = [Vector(), Vector(0, self.speed), Vector(0, -self.speed), Vector(self.speed, 0), Vector(-self.speed, 0)]
        self.velocity_arr = [Vector(0, self.speed), Vector(0, -self.speed)]

        # GeneticAlgorithm stuff
        self.dna = []

        # dna values (later dna will become a neural network):
        #  - speed reduction
        #  - fullness depletion rate
        #  - forage chance
        #  - eat chance
        #  - move up chance
        #  - move left chance
        #  - move right chance
        #  - move down chance
        #  - idle chance

        self.fitness = 0
        self.fitness_increment = 1
        self.mutation_rate = 0.1

        # stats
        self.fullness = 100

        # inventory
        self.food_count = 0
        self.food_limit = 2

    # return the action that the survivor wants to perform
    def predict(self):
        pass

    def mutate(self):
        pass

    def get_offspring_rate(self):
        pass

    def create_offspring(self, partner):
        pass

    def increase_fitness(self):
        self.fitness += self.fitness_increment

    def decrease_fullness(self):
        self.fullness -= 0.08  # randint(0, 20)  # 10  # get depletion rate from dna  randint(0, 20)

    def is_dead(self):
        return self.fullness <= 0

    def give_food(self):
        self.food_count = min(self.food_count + 1, self.food_limit)

    # TODO: See if I need acceleration
    def move(self):
        if not self.is_dead():
            #self.position.add(self.velocity)
            self.position.add(random.choice(self.velocity_arr))
