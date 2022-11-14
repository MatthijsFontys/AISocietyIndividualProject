import pickle
import gzip
import neat
from world.map.map_checkpoint import MapCheckpoint

SUFFIX = '-meta'

class MyCheckpointer(neat.Checkpointer):

    def __init__(self, map_data: MapCheckpoint, generation_interval=100, time_interval_seconds=300, filename_prefix='neat-checkpoint-'):
        self.map_data = map_data
        super().__init__(generation_interval, time_interval_seconds, filename_prefix)

    def save_checkpoint(self, config, population, species_set, generation):
        super().save_checkpoint(config, population, species_set, generation)
        filename = '{0}{1}{2}'.format(self.filename_prefix, generation, SUFFIX)
        with open(filename, 'wb') as save_file:
            pickle.dump(self.map_data, save_file)

    @staticmethod
    def restore_checkpoint(filename):
        population = neat.Checkpointer.restore_checkpoint(filename)
        with open(filename + SUFFIX, 'rb') as save_file:
            map_cp: MapCheckpoint = pickle.load(save_file)
            return population, map_cp



