import math
from util.vector_pool import VectorPool
from entities.entity_enums import EntityType


# Grid datastructure
# [x, y, {EntityType: [entities in grid cell]}]
#
#
#
class CollisionGrid:

    def __init__(self, cell_size, world_width, world_height, trees):
        self.width = math.floor(world_width / cell_size)
        self.height = math.floor(world_height / cell_size)
        self.cell_size = cell_size
        self.grid = [[{t.name: [] for t in EntityType} for x in range(self.width)] for y in range(self.height)]
        self.nearby_directions = []
        self.vector_pool = VectorPool()
        for i in range(-1, 2):
            for j in range(-1, 2):
                self.nearby_directions.append([i, j])

        for tree in trees:
            x_index = self.position_to_index(tree.position.x)
            y_index = self.position_to_index(tree.position.y)
            self.grid[x_index][y_index][EntityType.TREE.name].append(tree)

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

        for tree in self.get_nearby_entities(x, y, entity_type):
            distance = tree.position.get_distance_squared(position, self.vector_pool.lend())
            if distance < record_distance:
                record_distance = distance
                record_entity = tree

        self.vector_pool.release(position)
        return record_entity

    # helper methods
    def is_in_grid(self, x_index, y_index):
        return 0 <= x_index < self.width and 0 <= y_index < self.height

    def position_to_index(self, position):
        return math.floor(position / self.cell_size)
