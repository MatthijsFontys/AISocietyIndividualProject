from abc import ABC, abstractmethod
import typing

from drawing.entity_painter import EntityPainter
from drawing.sprites.entity_sprite_base import EntitySpriteBase
from world.map.map_dto import MapDto
from util.vector import Vector


class EntityBase(ABC):

    def __init__(self, data_collector=None):
        self.data_collector = data_collector
        self.position: typing.Optional[Vector] = None
        self.sprite = None

    @abstractmethod
    def tick(self, map_dto: MapDto):
        pass

    def set_data_collector(self, data_collector):
        if self.data_collector is None:
            self.data_collector = data_collector

    @abstractmethod
    def get_input_value(self) -> int:
        pass

    def get_sprite(self, entity_painter: EntityPainter):
        if self.sprite is None:
            self.sprite = self.init_sprite(entity_painter)
        return self.sprite

    @abstractmethod
    def init_sprite(self, entity_painter: EntityPainter) -> EntitySpriteBase:
        pass
