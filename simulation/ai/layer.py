import math
import random
import numpy as np


class Layer:

    def __init__(self, input_count, node_count):
        # weight dimensions = (rows * columns) (nodes_in_layer * inputs)
        self.input_count = input_count
        self.node_count = node_count
        self.weights = []

        # initialize the weights with random values between -1 and 1
        for i in range(node_count):
            self.weights.append([])
            for j in range(input_count):
                self.weights[i].append(random.uniform(-1, 1))
        #print(self.weights)
        # self.bias = []  # idk about this yet

    def activate(self, values):
        # sigmoid
        return list(map(lambda x: 1 / (1 + math.exp(-x)), values))

    def feed_forward(self, inputs):
        values = np.matmul(self.weights, inputs)
        return self.activate(values)

