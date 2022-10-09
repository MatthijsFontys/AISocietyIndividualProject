import random
import neat
import os
from ai.neuralnetwork import NeuralNetwork
from snake_ai.game import Game
from snake_ai.gen_info import GenerationInfo


class NeatStrat:

    def __init__(self, cols, start_new=True):
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, 'neat-config')
        self.CONFIG: neat.Config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                               neat.DefaultStagnation, config_path)
        # Add a stdout reporter to show progress in the terminal.
        self.neat_population = neat.checkpoint.Checkpointer.restore_checkpoint('neat-checkpoint-7715') #neat.Population(self.CONFIG)
        #self.neat_population = neat.Population(self.CONFIG)
        self.neat_population.add_reporter(neat.StdOutReporter(False))
        # self.neat_population.add_reporter(neat.StatisticsReporter())
        self.neat_population.add_reporter(neat.Checkpointer(501))

        self.SIGNATURE = 'NEAT'
        self.COLS = cols
        # self.population_size = 250
        self.data_collector = None
        self.min_fps = 10
        self.max_fps = 1000

        self.start_new = start_new

    def create_brain(self, genome):
        return neat.nn.FeedForwardNetwork.create(genome, self.CONFIG)

    def save_population(self, population):
        pass

    def get_saved_population(self, genomes):
        self.start_new = True
        return self.get_initial_population(genomes)

    def get_initial_population(self, genomes):
        if self.start_new:
            return [Game(self.COLS, self.create_brain(g), g) for _, g in genomes]
        else:
            return self.get_saved_population(genomes)

    def score_genomes(self, population):
        for p in population:
            p.genome.fitness = p.get_score()

    def repopulate(self, population):
        return self.get_initial_population([(1, population[0].genome)])

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
