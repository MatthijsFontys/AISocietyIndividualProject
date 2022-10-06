import numpy as np
import random
from ai.neuralnetwork import NeuralNetwork
from snake_ai.game import Game
from snake_ai.gen_info import GenerationInfo


class MyDefaultStrat:

    def __init__(self, cols, population_size=250, start_new=False):
        self.SIGNATURE = 'DEFAULT_INPUT'
        self.COLS = cols
        self.data_collector = None
        self.min_fps = 10
        self.max_fps = 1000

        self.population_size = population_size
        self.start_new = start_new

    def create_brain(self):
        return NeuralNetwork(11, 4).add_layer(12).add_layer(12).build()

    def save_population(self, population):
        for i, game in enumerate(population):
            game.brain.save(f'{self.SIGNATURE}_brain_{i}')

    def get_saved_population(self):
        #return [Game(self.COLS, NeuralNetwork.load(f'location_input_no_collision/{self.SIGNATURE}_brain_{i}')) for i in range(self.population_size)]
        return [Game(self.COLS, NeuralNetwork.load(f'location_input_no_collision/brain_{i}')) for i in range(self.population_size)]

    def get_initial_population(self):
        if self.start_new:
            return [Game(self.COLS, self.create_brain()) for _ in range(self.population_size)]
        else:
            return self.get_saved_population()

    def repopulate(self, population):
        info = GenerationInfo(population)
        new_population = []
        for _ in enumerate(population):
            try_counter = 0
            parent_a = self.pick_parent(population, info)
            parent_b = self.pick_parent(population, info)
            while parent_a == parent_b and try_counter < 1000:
                parent_b = self.pick_parent(population, info)
                try_counter += 1

            offspring = Game(self.COLS, self.create_brain())
            # offspring.brain = GeneticNeurolab.cross_over(parent_a.brain, parent_b.brain)
            offspring.brain.cross_over(parent_a.brain, parent_b.brain)
            new_population.append(offspring)
        return new_population

    def feed_forward(self, game):
        inputs = self.get_inputs(game)
        outputs = game.brain.feed_forward(inputs)
        highest = max(outputs)
        return outputs.index(highest)

    # would be private methods - not part of every strategy
    def get_inputs(self, game):
        inputs = [
                  # Snake direction
                  (game.snake.movement_index / 3),
                  # Snake head position
                  game.snake.pos.x / (self.COLS - 1),
                  game.snake.pos.y / (self.COLS - 1),
                  # Food position
                  max(game.snake.pos.y - game.food.y, 0) / (self.COLS - 1),
                  max(game.food.y - game.snake.pos.y, 0),
                  max(game.food.x - game.snake.pos.x, 0),
                  max(game.snake.pos.x - game.food.x, 0),
                  # Rest of body position
                  *self.get_segment_inputs(game)
                  ]
        return inputs

    def get_segment_inputs(self, game):
        left_record = right_record = up_record = down_record = self.COLS - 1
        for segment in game.snake.segments:
            if segment.y == game.snake.pos.y:
                delta = game.snake.pos.x - segment.x
                if delta > 0:
                    left_record = min(delta, left_record)
                else:
                    right_record = min(abs(delta), right_record)
            elif segment.x == game.snake.pos.x:
                delta = game.snake.pos.y - segment.y
                if delta > 0:
                    up_record = min(delta, up_record)
                else:
                    down_record = min(abs(delta), down_record)
        output = map(lambda x: x / (self.COLS - 1), [left_record, right_record, up_record, down_record])
        return list(output)

    def pick_parent(self, population, gen_info):
        rand = random.random()
        for member in population:
            rand -= member.get_score() / gen_info.summed_score
            if rand <= 0:
                return member
        print('No parent found!')
        return random.choice(population)

