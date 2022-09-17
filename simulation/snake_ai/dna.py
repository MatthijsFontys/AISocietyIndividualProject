import random


class Dna:

    def __init__(self, grid_size):
        self.index = 0
        self.data = []
        for i in range(500):
            self.data.append(random.randint(0, 3))

    def predict(self):
        value = self.data[self.index]
        self.index += 1
        if self.index >= len(self.data):
            self.index = 0
        return value

    def cross_over(self, parent_a, parent_b):
        parents = [parent_a, parent_b]
        for i in range(len(self.data)):
            self.data[i] = random.choice(parents).data[i]
            self.data[i] = self.get_mutated_value(self.data[i])

    def get_mutated_value(self, start_value):
        if random.random() < 0.01:
            return random.randint(0, 3)
        else:
            return start_value

