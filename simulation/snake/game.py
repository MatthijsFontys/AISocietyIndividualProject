from random import randrange
from math import floor
from dna import Dna
from ai.neuralnetwork import NeuralNetwork
from food_dna import FoodDna

# actual ff library
import neurolab as nl
import numpy as np
from ai.genetic_nl import GeneticNeurolab




class Game:

    def __init__(self, win_size, grid_size):
        #self.brain = Dna(grid_size)
        #self.brain = NeuralNetwork(2, 4).add_layer(8).add_output_layer()
        self.brain = nl.net.newff([[0, 1], [0, 1], [0, 1], [0, 1]], [5, 4])
        self.remove_score = False
        self.food_brain = FoodDna(grid_size)
        self.WIN_SIZE = win_size
        self.GRID_SIZE = grid_size
        self.COLS = floor(win_size / grid_size)
        self.speed = 1
        self.is_alive = True
        # 0 = up, 1 = down, 2 = left, 3 = right
        self.MOVEMENT = [[0, -self.speed], [0, self.speed], [-self.speed, 0], [self.speed, 0]]
        #self.snake = [self.get_random_location()]
        self.snake = [[floor(self.COLS / 2), floor(self.COLS / 2)]]
        self.time_alive = 0
        self.movement_index = 0
        self.food_location = self.get_random_no_snake_location()
        self.exploration_score = 1
        self.visited = [[False for x in range(self.COLS + 100)] for y in range(self.COLS + 100)]

    def choose_direction_index(self):
        inputs = [
                  #(self.movement_index + 1) / 4,
                  self.snake[0][0] / (self.COLS - 1),
                  self.snake[0][1] / (self.COLS - 1),
                  # self.snake[0][0],
                  # self.snake[0][1]
                  # (self.food_location[0] - self.snake[0][0]) / (self.COLS - 1),
                  # (self.food_location[1] - self.snake[0][1]) / (self.COLS - 1)
                  (self.food_location[0]) / (self.COLS - 1),
                  (self.food_location[1]) / (self.COLS - 1)
                  ]
        # return self.brain.predict()
        # outputs = self.brain.feed_forward(inputs)

        outputs = self.brain.sim([inputs])
        # get the highest output as the direction index
        outputs = outputs.tolist()[0]
        highest = max(outputs)
        #print(inputs, outputs, outputs.index(highest))
        #print(self.snake[0][0], self.snake[0][1]) # from 0 to 12
        # print('CHOSEN INDEX: ', outputs.index(highest))
        return outputs.index(highest)

    def move_in_direction(self, movement_index):
        # snake can't move in the opposite direction that it is going
        # the only way the breaking sums are reached is when the opposite direction index is chosen
        movement_sum = self.movement_index + movement_index

        # temp for testing
        prev_index = self.movement_index
        self.movement_index = movement_index
        if self.MOVEMENT[movement_index][0] == 0 and self.MOVEMENT[prev_index][0] == 0:
            if self.MOVEMENT[movement_index][1] != self.MOVEMENT[prev_index][1]:
                self.movement_index = prev_index
        elif self.MOVEMENT[movement_index][1] == 0 and self.MOVEMENT[prev_index][1] == 0:
            if self.MOVEMENT[movement_index][0] != self.MOVEMENT[prev_index][0]:
                self.movement_index = prev_index



        # if 1 < movement_sum < 4 or True:
        #     self.movement_index = movement_index
        #     self.exploration_score += 1

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
        # print(len(self.visited), len(self.visited[0]))
        print(self.snake[0][0], self.snake[0][1])
        self.visited[max(self.snake[0][0], 0)][max(self.snake[0][1], 0)] = True

    def try_eat_food(self, food_locations):
        if self.snake[0][0] == self.food_location[0] and self.snake[0][1] == self.food_location[1]:
            #self.food_location = self.get_random_no_snake_location()
            # self.food_location = self.food_brain.predict()
            self.food_location = self.get_random_no_snake_location()  # food_locations[len(self.snake) % len(food_locations)]
            self.snake.append([0, 0])

    def is_game_over(self):
        is_out_of_bounds = self.snake[0][0] >= self.COLS or \
                           self.snake[0][0] <= 0 or \
                           self.snake[0][1] >= self.COLS or \
                           self.snake[0][1] <= 0

        is_stuck = self.time_alive > len(self.snake) * 600
        if is_stuck:
            self.remove_score = True
        does_overlap = False
        for i in range(1, len(self.snake)):
            segment = self.snake[i]
            does_overlap = self.snake[0][0] == segment[0] and self.snake[0][1] == segment[1]
            if does_overlap:
                break
        self.is_alive = not (is_out_of_bounds or does_overlap or is_stuck)
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
        # todo: remove the -1 and +2 when neural network is added so the food can spawn near the edges again
        return [randrange(floor(self.WIN_SIZE / self.GRID_SIZE - 2)) + 1, randrange(floor(self.WIN_SIZE / self.GRID_SIZE - 2)) + 1]

    def get_score(self):
        snake_len = len(self.snake) - 1
        visited_score = 0
        for x in range(self.COLS):
            for y in range(self.COLS):
                if self.visited[x][y]:
                    visited_score += 1

        score = snake_len * 1000 + visited_score#+ self.exploration_score * 6
        # if self.remove_score:
        #     return 1
        #return score
        #return pow(len(self.snake)
        return pow(score, 2) + 1
        #return self.exploration_score
        # return self.time_alive * self.time_alive + self.exploration_score


    # TODO: remove later when dna is neural network and food is random again
    def set_initial_food(self, food_locations):
        self.food_location = food_locations[0]
