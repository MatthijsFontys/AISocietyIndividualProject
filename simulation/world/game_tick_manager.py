# manages everything in the world that doesn't need to be updated every frame
# for now should help with fruit regrowth and increasing survivor fitness

# the only thing that needs to be updated every frame and thus not managed by game ticks are the player's actions
import random
from entities.survivor import Survivor
from util.vector import Vector
from drawing.survivor_painter import SurvivorSprite
from world.world_map import WorldMap


class GameTickManager:

    def __init__(self, world):
        self.tick_interval = 10
        self.tick_counter = 0
        self.map: WorldMap = world

    def tick(self):

        self.tick_counter += 1
        if self.tick_counter >= self.tick_interval:
            for tree in self.map.trees:
                tree.tick()

            # reversed so that elements can be removed while looping through
            for survivor in reversed(self.map.population):
                survivor.increase_fitness()
                survivor.decrease_fullness()
                if survivor.is_dead():
                    self.map.population.remove(survivor)

            self.tick_counter = 0


            # check and create offspring TODO: for now in this class, obviously should go into another class eventually (but still be managed by ticks)
            # todo: remove hardcoded world size
            if random.random() < 0.5:
                offspring = Survivor(Vector(random.randrange(self.map.WIDTH), random.randrange(self.map.HEIGHT)))
                parent_a = None
                parent_b = None
                best_survivors = sorted(self.map.population, key=lambda x: x.fitness, reverse=True)
                middle_index = len(best_survivors) // 2
                best_survivors = best_survivors[:middle_index]

                while parent_a == parent_b:
                    parent_a = random.choice(best_survivors)
                    parent_b = random.choice(best_survivors)

                offspring.brain.cross_over(parent_a.brain, parent_b.brain)
                self.map.population.append(offspring)
