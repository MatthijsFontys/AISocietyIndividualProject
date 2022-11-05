# manages everything in the world that doesn't need to be updated every frame
# for now should help with fruit regrowth and increasing survivor fitness

# the only thing that needs to be updated every frame and thus not managed by game ticks are the player's actions
import random
from entities.survivor import Survivor
from util.vector import Vector
from world.overworld_map import OverworldMap
from world.tick_counter import TickCounter
from world.waiting_map import WaitingMap
from entities.entity_enums import EntityType


class GameTickManager:

    def __init__(self, world: OverworldMap, wait_world: WaitingMap):
        self.MAP = world
        self.WAIT_MAP = wait_world
        self.MAPS = [self.MAP, self.WAIT_MAP]

        self.tick_counter = TickCounter(10)
        self.day_counter = TickCounter(100)
        self.day = 1

    def tick(self):
        if not self.tick_counter.tick():
            return

        if self.day_counter.tick():
            self.day += 1

        for world in self.MAPS:
            for t in EntityType:
                for entity in reversed(world.get_entities(t)):
                    entity.tick(world.dto)

        # Chance to bring offspring from waiting room
        if random.random() < 0.15:
            offspring = self.WAIT_MAP.dequeue()
            if offspring is not None:
                self.MAP.population.append(offspring)

    def get_day_percent(self):
        return self.day_counter.get_percentage()

    def get_days_precise(self):
        return self.day + self.get_day_percent()

