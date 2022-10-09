from random import randint
from math import floor

import numpy as np

from snake import Snake
from util.vector import Vector
from ai.neuralnetwork import NeuralNetwork
# actual FeedForward library
import neurolab as nl


class Game:

    def __init__(self, cols, brain, genome=None):
        self.COLS = cols
        self.brain = brain
        #nl.net.newff([[0, 1], [0, 1], [0, 1], [-1, 1], [-1, 1]], [10, 10, 4])
        input_count = cols * cols + 7
        self.brain = brain
        self.snake = Snake(floor(self.COLS / 2), floor(self.COLS / 2))
        self.food = self.get_random_no_snake_location()
        # scoring
        self.is_stuck = 0
        self.time_alive = 0
        self.food_proximity_score = 0

        # Preventing looping snakes
        self.path = []
        self.banned_path = []

        # Neat
        self.genome = genome

    def move_in_direction(self, movement_index):
        self.snake.move(movement_index)
        proximity_score = 2
        delta = Vector.subtract_new(self.snake.pos, self.food)
        proximity_score -= abs(delta.x) / (self.COLS - 1)
        proximity_score -= abs(delta.y) / (self.COLS - 1)
        self.food_proximity_score += proximity_score
        index = self.get_path_index(self.snake.pos)
        self.path.append(self.snake.pos.copy())
        if self.is_banned_path():
            self.is_stuck += 1
            return
        if index != -1 and len(self.path) > 2:
            self.banned_path = self.path[index:]
            self.path = []

    def try_eat_food(self):
        if self.snake.pos.equals(self.food):
            self.food = self.get_random_no_snake_location()
            self.snake.eat()
            self.is_stuck = 0
            self.path = []
            self.banned_path = []

    def is_alive(self):
        is_out_of_bounds = self.snake.pos.x > self.COLS - 1 or \
                           self.snake.pos.x < 0 or \
                           self.snake.pos.y > self.COLS - 1 or \
                           self.snake.pos.y < 0

        # Todo: encapsulate does overlap in a function instead, can be reused for placing food
        does_overlap = False
        for i in range(1, self.snake.size()):
            segment = self.snake.get_segment(i)
            does_overlap = self.snake.pos.equals(segment)
            if does_overlap:
                break
        return not (is_out_of_bounds or self.is_stuck > 2 or does_overlap)  # Todo re-add overlap when the learning is working better # and add stuck when not in cinema mode

    def get_random_location(self):
        return Vector(randint(0, self.COLS - 1), randint(0, self.COLS - 1)) # Todo make this 0, self.COLS - 1 again when the snake is trained better

    def get_random_no_snake_location(self):
        picked_pos = self.get_random_location()
        while any(pos.equals(picked_pos) for pos in self.snake.segments) or self.snake.pos.equals(picked_pos):
            picked_pos = self.get_random_location()
        return picked_pos

    def get_score(self):
        score = self.get_normalized_score()
        return score ** 2

    def get_normalized_score(self):
        snake_len = max(self.snake.size() - 2, 0)
        score = snake_len * 100 + floor(1 * self.food_proximity_score)
        if self.is_stuck > 2:
            score /= 5
        return max(1, score)

    def get_path_index(self, vector: Vector):
        for i, pos in enumerate(self.path):
            if pos.equals(vector):
                return i
        return -1

    def is_banned_path(self):
        if len(self.banned_path) != len(self.path):
            return False
        for i, pos in enumerate(self.path):
            if pos.x != self.path[i].x or pos.y != self.path[i].y:
                return False
        return True

    def reset(self):
        self.snake = Snake(floor(self.COLS / 2), floor(self.COLS / 2))
        self.food = self.get_random_location()
        # scoring
        self.is_stuck = False
        self.time_alive = 0
        self.food_proximity_score = 0

