import random
from util.vector import Vector


class AgentDna:

    def __init__(self, size=100):
        # Agent movement
        self.SPEED = 1
        self.MOVEMENT = [Vector(0, -self.SPEED), Vector(0, self.SPEED), Vector(-self.SPEED, 0), Vector(self.SPEED, 0)]
        self.MUTATION_RATE = 0.025
        self.EMPTY = Vector()
        # Agent data
        self.data = [Vector()]
        self.index = 1
        for i in range(size):
            self.data.append(random.choice(self.MOVEMENT))

    def next(self):
        if self.index < len(self.data):
            self.index += 1
            return self.data[self.index - 1]
        else:
            return self.EMPTY

    def cross_over(self, parent_a, parent_b):
        parents = [parent_a, parent_b]
        for i in range(len(self.data)):
            self.data[i] = random.choice(parents).data[i]
            self.data[i] = self.get_mutated_value(self.data[i])
        self.data[0] = Vector()

    def get_mutated_value(self, start_value):
        if random.random() <= self.MUTATION_RATE:
            return random.choice(self.MOVEMENT)
        else:
            return start_value

    def get_moves_remaining(self):
        return max(0, len(self.data) - self.index)

