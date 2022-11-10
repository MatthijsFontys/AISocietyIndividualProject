from ai.my_neat import MyNeat
from entities.survivor import Survivor
from world.data_enums import GlobalMetric
from world.world_map import WorldMap
from map_creator.map_save import MapSave
from world.data_collector import DataCollector

"""
The map that is actually going to be visible to the user
"""


class OverworldMap(WorldMap):

    def __init__(self, save: MapSave, population_size, cell_size):
        super().__init__(save, population_size, cell_size)
        self.did_populate = False
        self.data_collector = None

    def set_data_collector(self, data_collector: DataCollector):
        if self.data_collector is None:
            self.data_collector = data_collector

    # Returns true if populated when the method was called, false if populated already
    def try_populate(self, genomes, neat: MyNeat):
        to_return = not self.did_populate
        if not self.did_populate:
            for _, genome in genomes:
                self.population.append(Survivor(self.get_rand_position(), genome, neat.create_brain(genome)))
            self.did_populate = True
        return to_return

    def birth(self, offspring: Survivor):
        offspring.start_exist()
        self.population.append(offspring)
        self.data_collector.add_data(GlobalMetric.BIRTHS)
