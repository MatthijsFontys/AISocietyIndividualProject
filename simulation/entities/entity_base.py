from abc import ABC, abstractmethod

from world.map.map_dto import MapDto


class EntityBase(ABC):

    def __init__(self, data_collector=None):
        self.data_collector = data_collector

    @abstractmethod
    def tick(self, map_dto: MapDto):
        pass

    def set_data_collector(self, data_collector):
        if self.data_collector is None:
            self.data_collector = data_collector

