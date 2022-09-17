from random import randint
from math import floor
from snake import Snake
from util.vector import Vector

# actual FeedForward library
import neurolab as nl


class Game:

    def __init__(self, cols):
        self.COLS = cols
        self.REGION_MAP = [[1, 3], [2, 4]]
        inputs = 4
        self.brain = nl.net.newff([[0, 1] for x in range(inputs)], [10, 4])
        self.snake = Snake(floor(self.COLS / 2), floor(self.COLS / 2))
        self.food = self.get_random_location()
        # scoring
        self.time_alive = 0
        self.regions_visited = 0
        self.grid = [[False for x in range(self.COLS)] for y in range(self.COLS)]
        self.region = self.get_region()

    def choose_direction_index(self):
        inputs = [
                  self.snake.pos.x,
                  self.snake.pos.y,
                  self.food.x / (self.COLS - 1),
                  self.food.y / (self.COLS - 1)
                  ]

        # running the neural network
        outputs = self.brain.sim([inputs])

        # get the highest output as the direction index
        outputs = outputs.tolist()[0]
        highest = max(outputs)

        return outputs.index(highest)

    def move_in_direction(self, movement_index):
        self.snake.move(movement_index)
        # region = self.get_region()
        # if region != self.region:
        #     self.region = region
        #     self.regions_visited += 1
        visited = self.grid[self.snake.pos.x][self.snake.pos.y]
        if not visited:
            self.regions_visited += 1
            self.grid[self.snake.pos.x][self.snake.pos.y] = True



    def try_eat_food(self):
        if self.snake.pos.x == self.food.x and self.snake.pos.y == self.food.y:
            self.food = self.get_random_location()
            self.snake.eat()

    def is_alive(self):
        is_out_of_bounds = self.snake.pos.x >= self.COLS - 1 or \
                           self.snake.pos.x <= 0 or \
                           self.snake.pos.y >= self.COLS - 1 or \
                           self.snake.pos.y <= 0

        is_stuck = self.time_alive > self.snake.size() * self.snake.size() * 100
        does_overlap = False
        for i in range(1, self.snake.size()):
            segment = self.snake.get_segment(i)
            does_overlap = self.snake.pos.x == segment.x and self.snake.pos.y == segment.y
            if does_overlap:
                break
        return not (is_out_of_bounds or is_stuck)  # Todo re-add overlap when the learning is working better

    def get_random_location(self):
        return Vector(randint(0, self.COLS - 1), randint(0, self.COLS - 1))

    def get_score(self):
        # score = 0
        # for x in range(self.COLS):
        #     for y in range(self.COLS):
        #         if self.grid[x][y]:
        #             score += 1
        # score / (self.COLS * self.COLS) * 100
        snake_len = self.snake.size() - 1
        score = snake_len * 1000 + self.regions_visited * 5 + 1
        return pow(score, 2)

    def get_region(self):
        x = y = 0
        cols = self.COLS - 1
        if self.snake.pos.x > floor(cols / 2):
            x += 1
        if self.snake.pos.y < floor(cols / 2):
            y += 1
        return self.REGION_MAP[x][y]
