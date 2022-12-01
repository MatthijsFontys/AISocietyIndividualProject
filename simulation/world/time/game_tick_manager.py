# manages everything in the world that doesn't need to be updated every frame
# for now should help with fruit regrowth and increasing survivor fitness

# the only thing that needs to be updated every frame and thus not managed by game ticks are the player's actions
import random
from world.time.game_tick_dto import GameTickDto
from world.map.overworld_map import OverworldMap
from world.time.tick_counter import TickCounter
from world.map.waiting_map import WaitingMap
from entities.entity_enums import EntityType


class GameTickManager:

    # Todo: somehow figure out how to start from a different day when loading a checkpoint
    def __init__(self):
        self.MAP = None
        self.WAIT_MAP = None
        self.MAPS = []
        self.tick_counter = TickCounter(10)
        # Todo: figure out a good amount of ticks each day, but 1500 at 60 fps shows each minute
        self.day_counter = TickCounter(1_500)
        self.day = 1
        self.dto = GameTickDto(self.day, self.day_counter)
        self.subscribers = [self.dto]

    def tick(self):
        if not self.tick_counter.tick():
            return

        if self.day_counter.tick():
            self.day += 1
            log = f' Starting day {self.day} '
            print(f' {log:*^{len(log) + 12}}')

        for world in self.MAPS:
            for t in EntityType:
                for entity in reversed(world.get_entities(t)):
                    entity.tick(world.dto)

        has_fired = self.day_counter.get_has_fired()

        for subscriber in self.subscribers:
            subscriber.tick(has_fired)

        # Todo: make this a separate class that subs to the tick manager | low prio
        # Chance to bring offspring from waiting room
        if random.random() < 0.15:
            offspring = self.WAIT_MAP.dequeue(self.day)
            if offspring is not None:
                self.MAP.birth(offspring)

    def set_world(self, world: OverworldMap, wait_world: WaitingMap):
        self.MAP = world
        self.WAIT_MAP = wait_world
        self.MAPS = [self.MAP, self.WAIT_MAP]

    def set_day(self, day: int):
        self.day = day
        self.dto.day = day

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
        self.subscribers.remove(subscriber)

    def get_day_percent(self):
        return self.day_counter.get_percentage()

    def get_days_precise(self):
        return self.day + self.get_day_percent()

