from entities.entity_enums import EntityType


class MapDto:

    # Map DTO to prevent circular dependencies and not share the entire world
    def __init__(self, entities, trees, population, saplings, campfires, width, height, population_size):
        self.WIDTH = width
        self.HEIGHT = height
        self.POPULATION_SIZE = population_size

        self.entities = entities
        self.trees = trees
        self.population = population
        self.saplings = saplings
        self.campfires = campfires

    def get_entities(self, t: EntityType):
        return self.entities.get(t.name)
