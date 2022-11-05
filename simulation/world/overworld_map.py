from ai.my_neat import MyNeat
from entities.survivor import Survivor
from world.collision_grid import CollisionGrid
from world.world_map import WorldMap
from drawing.camera import Camera
from map_creator.map_save import MapSave


class OverworldMap(WorldMap):

    def __init__(self, save: MapSave, population_size, cell_size):
        super().__init__(save, population_size, cell_size)
        self.did_populate = False

    # Returns true if populated when the method was called, false if populated already
    def try_populate(self, genomes, neat: MyNeat):
        to_return = not self.did_populate
        if not self.did_populate:
            for _, genome in genomes:
                self.population.append(Survivor(self.get_rand_position(), genome, neat.create_brain(genome)))
            self.did_populate = True
        return to_return
