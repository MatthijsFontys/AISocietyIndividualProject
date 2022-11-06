import math
from util.vector_pool import VectorPool
from entities.entity_enums import EntityType

# Grid datastructure
# [x, y, {EntityType: [entities in grid cell]}]
from world.map_dto import MapDto


class CollisionGrid:

    def __init__(self, cell_size: int, world_dto: MapDto):
        self.map = world_dto
        self.width = math.floor(self.map.WIDTH / cell_size)
        self.height = math.floor(self.map.HEIGHT / cell_size)
        self.cell_size = cell_size
        self.grid = self.rebuild()
        self.nearby_directions = []
        self.vector_pool = VectorPool()
        for i in range(-1, 2):
            for j in range(-1, 2):
                self.nearby_directions.append([i, j])

    """
    Rebuild the grid with updated positions
    :return the built grid for better syntax in constructor
    """
    def rebuild(self):
        self.grid = [[{t.name: [] for t in EntityType} for x in range(self.width)] for y in range(self.height)]
        for t in EntityType:
            for entity in self.map.get_entities(t):
                x_index = self.position_to_index(entity.position.x)
                y_index = self.position_to_index(entity.position.y)
                self.grid[x_index][y_index][t.name].append(entity)
        return self.grid

    # Todo: fix what is going wrong here, why do I not find any survivors
    def get_nearby_entities(self, x, y, entity_type):
        nearby_entities = []
        start_x = self.position_to_index(x)
        start_y = self.position_to_index(y)

        for directions in self.nearby_directions:
            x_index = start_x + directions[0]
            y_index = start_y + directions[1]
            # don't check outside the edges of the grid
            if self.is_in_grid(x_index, y_index):
                nearby_entities.extend(self.grid[x_index][y_index][entity_type.name])

        return nearby_entities

    def get_closest_entity(self, x, y, entity_type):
        position = self.vector_pool.acquire(x, y)
        record_distance = math.inf
        record_entity = None

        for entity in self.get_nearby_entities(x, y, entity_type):
            distance = entity.position.get_distance_squared(position, self.vector_pool.lend())
            if distance < record_distance:
                record_distance = distance
                record_entity = entity

        self.vector_pool.release(position)
        return record_entity

    # helper methods
    def is_in_grid(self, x_index, y_index):
        return 0 <= x_index < self.width and 0 <= y_index < self.height

    def position_to_index(self, position):
        return math.floor(position / self.cell_size)
