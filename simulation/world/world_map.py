from entities.entity_enums import EntityType
from map_creator.map_save import MapSave


class WorldMap:

    def __init__(self, save: MapSave):
        self.WIDTH = save.width
        self.HEIGHT = save.height

        self.time_perception = -1
        self.spawn_points = []

        # Entities
        self.entities = {t.name: [] for t in EntityType}
        # Todo: might decouple all entities

