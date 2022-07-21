from random import randrange
from math import floor
from dna import Dna


class Game:

    def __init__(self, win_size, grid_size):
        self.brain = Dna(grid_size)
        self.WIN_SIZE = win_size
        self.GRID_SIZE = grid_size
        self.speed = 1
        self.is_alive = True
        # 0 = up, 1 = down, 2 = left, 3 = right
        self.MOVEMENT = [[0, -self.speed], [0, self.speed], [-self.speed, 0], [self.speed, 0]]
        #self.snake = [self.get_random_location()]
        self.snake = [[7, 7]]
        self.time_alive = 0
        self.movement_index = 0
        self.food_location = self.get_random_no_snake_location()

    def choose_direction_index(self):
        inputs = [self.snake[0][0] / self.GRID_SIZE,
                  self.snake[0][1] / self.GRID_SIZE,
                  # (self.food_location[0] - self.snake[0][0] / self.GRID_SIZE),
                  # (self.food_location[1] - self.snake[0][1] / self.GRID_SIZE)
                  ]
        return self.brain.predict()
        # outputs = self.brain.predict(inputs)
        # # get the highest output as the direction index
        # highest = max(outputs)
        # return outputs.index(highest)

    def move_in_direction(self, movement_index):
        # snake can't move in the opposite direction that it is going
        # the only way the breaking sums are reached is when the opposite direction index is chosen
        movement_sum = self.movement_index + movement_index
        if 1 < movement_sum < 4:
            self.movement_index = movement_index

        # update snake position
        direction = self.MOVEMENT[self.movement_index]
        # loops through the segments the 0 and 1 index in the loop are for the x and y of that segment
        for i, segment in reversed(list(enumerate(self.snake))):
            if i != 0:
                segment[0] = self.snake[i - 1][0]
                segment[1] = self.snake[i - 1][1]
            else:
                segment[0] += direction[0]
                segment[1] += direction[1]

    def try_eat_food(self):
        if self.snake[0][0] == self.food_location[0] and self.snake[0][1] == self.food_location[1]:
            self.food_location = self.get_random_no_snake_location()
            self.snake.append([0, 0])

    def is_game_over(self):
        is_out_of_bounds = self.snake[0][0] * self.GRID_SIZE > self.WIN_SIZE or \
                           self.snake[0][0] < 0 or \
                           self.snake[0][1] * self.GRID_SIZE > self.WIN_SIZE or \
                           self.snake[0][1] < 0
        does_overlap = False
        for i in range(1, len(self.snake)):
            segment = self.snake[i]
            does_overlap = self.snake[0][0] == segment[0] and self.snake[0][1] == segment[1]
            if does_overlap:
                break
        self.is_alive = not (is_out_of_bounds or does_overlap)
        return not self.is_alive

    def does_overlap_with_snake(self, location):
        does_overlap = False
        for segment in self.snake:
            does_overlap = location[0] == segment[0] and location[1] == segment[1]
            if does_overlap:
                break
        return does_overlap

    def get_random_no_snake_location(self):
        location = self.get_random_location()
        while self.does_overlap_with_snake(location):
            location = self.get_random_location()
        return location

    def get_random_location(self):
        return [randrange(floor(self.WIN_SIZE / self.GRID_SIZE)), randrange(floor(self.WIN_SIZE / self.GRID_SIZE))]

    def get_score(self):
        return len(self.snake) * 0 + self.time_alive

