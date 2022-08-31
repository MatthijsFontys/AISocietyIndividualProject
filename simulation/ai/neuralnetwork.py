import random
from ai.layer import Layer


class NeuralNetwork:

    def __init__(self, input_count, output_count):
        self.input_count = input_count
        self.output_count = output_count
        self.layers = []

    def add_layer(self, node_count):
        input_count = self.input_count
        if len(self.layers) > 0:
            input_count = self.layers[-1].node_count
        self.layers.append(Layer(input_count, node_count))
        return self

    def add_output_layer(self):
        self.layers.append(Layer(self.layers[-1].node_count, self.output_count))
        return self

    def feed_forward(self, inputs):
        for layer in self.layers:
            inputs = layer.feed_forward(inputs)
        return inputs

    # Genetic algorithm stuff
    def cross_over(self, parent_a, parent_b):
        for layer_index in range(len(self.layers)):
            my_layer = self.layers[layer_index]
            parent_layers = [parent_a.layers[layer_index], parent_b.layers[layer_index]]
            #parent_layers = [parent_a.layers[layer_index]]
            for i in range(self.layers[layer_index].node_count):
                parent_bias = random.choice(parent_layers).biases[i]
                my_layer.biases[i] = parent_bias
                my_layer.biases[i] = self.get_mutated_value(my_layer.biases[i])

                for j in range(self.layers[layer_index].input_count):
                    parent_weights = random.choice(parent_layers).weights[i][j]
                    my_layer.weights[i][j] = parent_weights
                    # mutation
                    my_layer.weights[i][j] = self.get_mutated_value(my_layer.weights[i][j])

    def get_mutated_value(self, start_value):
        sine = [1, -1]
        if random.random() < 0.015:
            #return start_value + random.uniform(-0.3, 0.3)
            # return  start_value + ((random.random() * 2 - 1) / 3)
            return start_value + (random.random() / 2 * random.choice(sine))
        else:
            return start_value
