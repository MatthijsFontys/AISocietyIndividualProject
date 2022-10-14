import pickle
import random
import neat
import os

import numpy as np

from ai.neuralnetwork import NeuralNetwork
from snake_ai.game import Game
from snake_ai.gen_info import GenerationInfo


class NeatCinemaStrat:

    def __init__(self, cols):
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, 'neat-config')
        self.CONFIG: neat.Config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                               neat.DefaultStagnation, config_path)

        self.SIGNATURE = 'NEAT_CINEMA'
        self.COLS = cols
        self.population_size = 1
        self.data_collector = None
        self.min_fps = 10
        self.max_fps = 1000
        self.start_new = False

        self.should_run_pygame = True
        self.should_run_neat = False

    def create_brain(self, genome):
        return neat.nn.FeedForwardNetwork.create(genome, self.CONFIG)

    def save_population(self, population):
        pass

    def get_saved_population(self):
        return self.get_initial_population()

    def get_initial_population(self):
        with open(f'nets/trained/snake_60mil_winner.pkl', 'rb') as save_file:
            genome = pickle.load(save_file)
            return [Game(self.COLS,self.create_brain(genome), genome)]

    def score_genomes(self, population):
        for p in population:
            p.genome.fitness = p.get_score()

    def repopulate(self, population):
        genome = population[0].genome
        return [Game(self.COLS,self.create_brain(genome), genome)]

    def feed_forward(self, game):
        inputs = self.get_inputs(game)
        outputs = game.brain.activate(inputs)
        highest = max(outputs)
        return outputs.index(highest)

    # would be private methods - not part of every strategy
    def get_inputs(self, game):
        segment_inputs = self.get_segment_inputs(game)
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
            #*self.get_grid_inputs(game)
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

    def get_grid_inputs(self, game):
        grid = np.zeros(self.COLS * self.COLS).tolist()
        for segment in game.snake.segments:
            grid[self.COLS * segment.y + segment.x] = 1
        return grid

    def pick_parent(self, population, gen_info):
        rand = random.random()
        for member in population:
            rand -= member.get_score() / gen_info.summed_score
            if rand <= 0:
                return member
        print('No parent found!')
        return random.choice(population)
