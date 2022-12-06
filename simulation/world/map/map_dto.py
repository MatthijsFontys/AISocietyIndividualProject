from entities.entity_enums import EntityType


class MapDto:

    # Map DTO to prevent circular dependencies and not share the entire world
    def __init__(self, entities, trees, population, saplings, campfires, width, height, population_size, stat_loss):
        self.WIDTH = width
        self.HEIGHT = height
        self.POPULATION_SIZE = population_size

        self.entities = entities
        self.trees = trees
        self.population = population
        self.saplings = saplings
        self.campfires = campfires

        # 0 - hunger | 1 = temperature  is pass as array for reference type benefits
        self.stat_loss = stat_loss

    def get_entities(self, t: EntityType):
        return self.entities.get(t.name)

    def get_hunger_loss(self):
        return self.stat_loss[0]

    def get_temperature_loss(self):
        return self.stat_loss[1]
