from ai.my_neat import MyNeat
from entities.survivor import Survivor
from world.data.data_enums import GlobalMetric
from world.map.world_base import WorldBase
from map_creator.map_save import MapSave
from world.data.data_collector import DataCollector

"""
The map that is actually going to be visible to the user
"""


class OverworldMap(WorldBase):

    def __init__(self, save: MapSave, population_size, cell_size):
        super().__init__(save, population_size, cell_size)
        self.did_populate = False

    """
    :return true if populated when the method was called, false if populated already
    """
    def try_populate(self, genomes, neat: MyNeat) -> bool:
        to_return = not self.did_populate
        if not self.did_populate:
            for _, genome in genomes:
                self.population.append(Survivor(self.get_rand_position(), genome, neat.create_brain(genome), self.data_collector))
            self.did_populate = True
        return to_return

    def birth(self, offspring: Survivor):
        offspring.start_exist(self.data_collector)
        self.population.append(offspring)
        self.data_collector.add_data(GlobalMetric.BIRTHS)
