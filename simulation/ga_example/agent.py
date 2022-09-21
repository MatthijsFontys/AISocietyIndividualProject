from random import randint
from math import floor
from util.vector import Vector
from ga_example.agent_dna import AgentDna

class Agent:

    def __init__(self):
        # Movement
        self.pos = Vector()
        self.dna = AgentDna()
        # scoring
        self.score = 0

    def move(self):
        pass

    def is_alive(self):
        return True

    def get_score(self):
        return self.get_normalized_score()

    def get_normalized_score(self):
        return self.score



