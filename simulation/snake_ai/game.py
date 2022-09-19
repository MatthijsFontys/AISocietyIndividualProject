from random import randint
from math import floor
from snake import Snake
from util.vector import Vector

# actual FeedForward library
import neurolab as nl


class Game:

    def __init__(self, cols):
        self.COLS = cols
        #self.REGION_MAP = [[1, 3], [2, 4]]
        inputs = 4
        self.brain = nl.net.newff([[0, 1], [0, 1], [0, 1], [-1, 1], [-1, 1]], [10, 10, 4])
        self.snake = Snake(floor(self.COLS / 2), floor(self.COLS / 2))
        self.food = self.get_random_location()
        # scoring
        self.is_stuck = 0
        self.time_alive = 0
        self.food_proximity_score = 0

        # Preventing looping snakes
        self.path = []
        self.banned_path = []

    def choose_direction_index(self):
        inputs = [
                  (self.snake.movement_index / 3),
                  self.snake.pos.x / (self.COLS - 1),
                  self.snake.pos.y / (self.COLS - 1),
                  (self.food.x - self.snake.pos.x) / (self.COLS - 1),
                  (self.food.y - self.snake.pos.y) / (self.COLS - 1)
                  ]

        # running the neural network
        outputs = self.brain.sim([inputs])

        # get the highest output as the direction index
        outputs = outputs.tolist()[0]
        highest = max(outputs)

        return outputs.index(highest)

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
            self.food = self.get_random_location()
            self.snake.eat()
            self.is_stuck = 0
            self.path = []
            self.banned_path = []

    def is_alive(self):
        is_out_of_bounds = self.snake.pos.x > self.COLS - 1 or \
                           self.snake.pos.x < 0 or \
                           self.snake.pos.y > self.COLS - 1 or \
                           self.snake.pos.y < 0

        # is_stuck = self.time_alive > self.snake.size() * self.snake.size() * 100
        does_overlap = False
        for i in range(1, self.snake.size()):
            segment = self.snake.get_segment(i)
            does_overlap = self.snake.pos.equals(segment)
            if does_overlap:
                break
        return not (is_out_of_bounds or self.is_stuck > 2)  # Todo re-add overlap when the learning is working better # and add stuck when not in cinema mode

    def get_random_location(self):
        return Vector(randint(0, self.COLS - 1), randint(0, self.COLS - 1)) # Todo make this 0, self.COLS - 1 again when the snake is trained better

    def get_score(self):
        snake_len = max(self.snake.size() - 2, 0)
        score = snake_len * 100 + floor(0 * self.food_proximity_score)
        if self.is_stuck > 2:
            score /= 5
        return score * score * score + 1

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

