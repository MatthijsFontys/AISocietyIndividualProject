import pickle
from entities.entity_enums import EntityType
from map_creator.rename_unpickler import renamed_load
from util.vector import Vector


class MapSave:

    def __init__(self, name, width=-1):
        # Meta data
        self.name = name
        self.width = width
        self.height = self.width

        # World entities
        self.entities = {t.name: [] for t in EntityType}

    def add_entity(self, t: EntityType, location: Vector):
        self.entities.get(t.name).append(location)

    def get_entities(self, t: EntityType):
        return self.entities.get(t.name)

    def save(self):
        with open(f'maps/{self.name}.pkl', 'wb') as save_file:
            pickle.dump(self, save_file)

    @staticmethod
    def load(name):
        with open(f'map_creator/maps/{name}.pkl', 'rb') as save_file:
           return renamed_load(save_file)
