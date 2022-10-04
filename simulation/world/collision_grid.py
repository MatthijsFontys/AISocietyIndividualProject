import math
from util.vector_pool import VectorPool


class CollisionGrid:

    def __init__(self, cell_size, world_width, world_height, trees):
        self.width = math.floor(world_width / cell_size)
        self.height = math.floor(world_height / cell_size)
        self.cell_size = cell_size
        self.grid = [[[] for x in range(self.width)] for y in range(self.height)]
        self.nearby_directions = []
        self.vector_pool = VectorPool()
        for i in range(-1, 2):
            for j in range(-1, 2):
                self.nearby_directions.append([i, j])

        for tree in trees:
            x_index = self.position_to_index(tree.position.x)
            y_index = self.position_to_index(tree.position.y)
            self.grid[x_index][y_index].append(tree)

    def get_nearby_trees(self, x, y):
        nearby_trees = []
        start_x = self.position_to_index(x)
        start_y = self.position_to_index(y)

        for directions in self.nearby_directions:
            x_index = start_x + directions[0]
            y_index = start_y + directions[1]
            # don't check outside the edges of the grid
            if self.is_in_grid(x_index, y_index):
                nearby_trees.extend(self.grid[x_index][y_index])

        return nearby_trees

    def get_closest_tree(self, x, y):
        position = self.vector_pool.acquire(x, y)
        record_distance = 1000_000
        record_tree = None

        for tree in self.get_nearby_trees(x, y):
            distance = tree.position.get_distance(position)
            if distance < record_distance:
                record_distance = distance
                record_tree = tree

        self.vector_pool.release(position)
        return record_tree

    # helper methods
    def is_in_grid(self, x_index, y_index):
        return 0 <= x_index < self.width and 0 <= y_index < self.height

    def position_to_index(self, position):
        return math.floor(position / self.cell_size)


