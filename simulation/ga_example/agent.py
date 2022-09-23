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
        self.finish = grid_exit.copy()
        self.score = 100

    def move(self):
        if not self.reached_finish():
            self.pos.add(self.dna.next())

    def get_score(self):
        return self.get_normalized_score()

    def get_normalized_score(self):
        distance = abs((self.finish.x - self.pos.x)) + abs((self.finish.y - self.pos.y))
        score = 1 - distance / 100
        if self.reached_finish():
            score += 100
            score += 10 * self.dna.get_moves_remaining()
        return score

    def reached_finish(self):
        return self.pos.equals(self.finish)



