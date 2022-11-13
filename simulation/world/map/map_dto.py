from entities.entity_enums import EntityType


class MapDto:

    # Map DTO to prevent circular dependencies and not share the entire world
    def __init__(self, entities, trees, population, saplings, campfires, width, height, population_size, fullness_loss, temperature_loss):
        self.WIDTH = width
        self.HEIGHT = height
        self.POPULATION_SIZE = population_size

        self.entities = entities
        self.trees = trees
        self.population = population
        self.saplings = saplings
        self.campfires = campfires

        self.fullness_loss = fullness_loss
        self.temperature_loss = temperature_loss

    def get_entities(self, t: EntityType):
        return self.entities.get(t.name)
