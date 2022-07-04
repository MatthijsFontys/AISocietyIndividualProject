import math


class CollisionGrid:

    def __init__(self, cell_size, world_width, world_height, trees):
        self.width = math.floor(world_width / cell_size)
        self.height = math.floor(world_height / cell_size)
        self.cell_size = cell_size
        self.grid = [[[] for x in range(self.width)] for y in range(self.height)]
        self.nearby_directions = []
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
            if x_index >= 0 and x_index < self.width and y_index > 0 and y_index < self.height:
                nearby_trees.extend(self.grid[x_index][y_index])

        return nearby_trees

    def position_to_index(self, position):
        return math.floor(position / self.cell_size)


