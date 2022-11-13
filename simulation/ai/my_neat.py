import neat
import os


class MyNeat:

    def __init__(self, start_from_gen=0, run_pygame=True):
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, 'my-neat-config')
        self.CONFIG: neat.Config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                               neat.DefaultStagnation, config_path)
        self.checkpointer = neat.Checkpointer(10, filename_prefix='checkpoints/neat-checkpoint-')
        self.start_gen = start_from_gen
        if start_from_gen == 0:
            self.neat_population = neat.Population(self.CONFIG)
        else:
            self.neat_population = self.checkpointer.restore_checkpoint(filename=f'checkpoints/neat-checkpoint-{self.start_gen}')

        self.population_size = len(self.neat_population.population)
        self.should_run_pygame = run_pygame
        # Todo: could add statistics reporter
        self.neat_population.add_reporter(neat.StdOutReporter(False))
        self.neat_population.add_reporter(self.checkpointer)

    def create_brain(self, genome):
        return neat.nn.FeedForwardNetwork.create(genome, self.CONFIG)

    def feed_forward(self, survivor, inputs):
        outputs = survivor.brain.activate(inputs)
        highest = max(outputs)
        return outputs.index(highest)
