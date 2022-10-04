class World:

    def __init__(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height

        self.time_perception = -1
        self.spawn_points = []

        # Entities
        self.trees = []
        self.survivors = []

