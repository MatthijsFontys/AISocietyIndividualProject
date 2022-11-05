import neat
import os


class MyNeat:

    def __init__(self, start_new=True):
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, 'my-neat-config')
        self.CONFIG: neat.Config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                               neat.DefaultStagnation, config_path)
        self.start_new = start_new
        self.checkpointer = neat.Checkpointer(10)
        if start_new:
            self.neat_population = neat.Population(self.CONFIG)
        else:
            self.neat_population = self.checkpointer.restore_checkpoint(filename='neat-checkpoint-3059')

        # Todo: check if this works
        self.population_size = len(self.neat_population.population)

        # Todo: might add statistics reporter
        self.neat_population.add_reporter(neat.StdOutReporter(False))
        self.neat_population.add_reporter(self.checkpointer)

        self.should_run_pygame = True
        self.should_run_neat = True

    def create_brain(self, genome):
        return neat.nn.FeedForwardNetwork.create(genome, self.CONFIG)

    def feed_forward(self, survivor, inputs):
        outputs = survivor.brain.activate(inputs)
        highest = max(outputs)
        return outputs.index(highest)
