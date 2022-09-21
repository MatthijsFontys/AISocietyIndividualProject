from random import randint
from math import floor
from snake import Snake
from util.vector import Vector
from ai.neuralnetwork import NeuralNetwork
# actual FeedForward library
import neurolab as nl


class Game:

    def __init__(self, cols):
        self.COLS = cols
        #self.REGION_MAP = [[1, 3], [2, 4]]
        inputs = 4
        #self.brain = nl.net.newff([[0, 1], [0, 1], [0, 1], [-1, 1], [-1, 1]], [10, 10, 4])
        self.brain = NeuralNetwork(11, 4).add_layer(12).add_layer(12).build()
        self.snake = Snake(floor(self.COLS / 2), floor(self.COLS / 2))
        self.food = self.get_random_no_snake_location()
        # scoring
        self.is_stuck = 0
        self.time_alive = 0
        self.food_proximity_score = 0

        # Preventing looping snakes
        self.path = []
        self.banned_path = []

    def choose_direction_index(self):
        segment_inputs = self.get_segment_inputs()
        inputs = [
                  # Snake direction
                  (self.snake.movement_index / 3),
                  # Snake head position
                  self.snake.pos.x / (self.COLS - 1),
                  self.snake.pos.y / (self.COLS - 1),
                  # Food position
                  max(self.snake.pos.y - self.food.y, 0) / (self.COLS - 1),
                  max(self.food.y - self.snake.pos.y, 0),
                  max(self.food.x - self.snake.pos.x, 0),
                  max(self.snake.pos.x - self.food.x, 0),
                  # Rest of body position
                  # Left (x is lower, y is the same) pos.x - segment.x | positive
                  segment_inputs[0],
                  # Right (x is higher, y is the same) pos.x - segment.x | negative
                  segment_inputs[1],
                  # Up (y is lower, x is the same) pos.y - segment.y | positive
                  segment_inputs[2],
                  # Down (y is higher, x is the same) pos.y - segment.y | negative
                  segment_inputs[3],
                  ]

        # running the neural network
        #outputs = self.brain.sim([inputs])
        outputs = self.brain.feed_forward(inputs)

        # get the highest output as the direction index
        #outputs = outputs.tolist()[0]
        highest = max(outputs)
        return outputs.index(highest)


    # Todo: if i stick with this method, find a better name
    def get_segment_inputs(self):
        left_record = right_record = up_record = down_record = self.COLS - 1
        for segment in self.snake.segments:
            if segment.y == self.snake.pos.y:
                delta = self.snake.pos.x - segment.x
                if delta > 0:
                    left_record = min(delta, left_record)
                else:
                    right_record = min(abs(delta), right_record)
            elif segment.x == self.snake.pos.x:
                delta = self.snake.pos.y - segment.y
                if delta > 0:
                    up_record = min(delta, up_record)
                else:
                    down_record = min(abs(delta), down_record)
        output = map(lambda x: x / (self.COLS - 1), [left_record, right_record, up_record, down_record])
        return list(output)


    def move_in_direction(self, movement_index):
        self.snake.move(movement_index)
        proximity_score = 2
        delta = Vector.subtract_new(self.snake.pos, self.food)
        proximity_score -= abs(delta.x) / (self.COLS - 1)
        proximity_score -= abs(delta.y) / (self.COLS - 1)
        # self.food_proximity_score += proximity_score
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
        return score * score * score

    def get_normalized_score(self):
        snake_len = max(self.snake.size() - 2, 0)
        score = snake_len * 1 + floor(0 * self.food_proximity_score)
        if self.is_stuck > 2:
            score /= 5
        return score

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

