from abc import ABC, abstractmethod
import typing
from world.map.map_dto import MapDto
from util.vector import Vector


class EntityBase(ABC):

    def __init__(self, data_collector=None):
        self.data_collector = data_collector
        self.position: typing.Optional[Vector] = None

    @abstractmethod
    def tick(self, map_dto: MapDto):
        pass

    def set_data_collector(self, data_collector):
        if self.data_collector is None:
            self.data_collector = data_collector

    @abstractmethod
    def get_input_value(self) -> int:
        pass
