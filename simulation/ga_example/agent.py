from random import randint
from math import floor
from util.vector import Vector
from ga_example.agent_dna import AgentDna


class Agent:

    def __init__(self, cols, grid_entry, grid_exit):
        # Movement
        self.pos = grid_entry.copy()
        self.dna = AgentDna(cols * cols)
        self.moves_left = cols * cols
        # scoring
        self.finish: Vector = grid_exit.copy()
        self.score = 100

    def move(self):
        if not self.reached_finish():
            self.pos.add(self.dna.next())

    def get_score(self):
        return self.get_normalized_score() * self.get_normalized_score()

    def get_normalized_score(self):
        if self.reached_finish():
            return 100 + 10 * self.dna.get_moves_remaining()
        else:
            distance = self.finish.get_distance(self.pos)
            return max(1, 20 - distance)

    def reached_finish(self):
        return self.pos.equals(self.finish)



