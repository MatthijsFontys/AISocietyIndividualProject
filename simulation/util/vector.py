import math

# TODO: replace this class with an actual vector class from some library

class Vector:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def add(self, vector):
        self.x += vector.x
        self.y += vector.y

    def subtract(self, vector):
        self.x -= vector.x
        self.y -= vector.y

    def scale(self, scalar):
        self.x *= scalar
        self.y *= scalar

    def normalize(self):
        self.scale(1 / self.get_magnitude())

    def get_magnitude(self):
        a_squared = self.x ** 2
        b_squared = self.y ** 2
        return math.sqrt(a_squared + b_squared)

    def get_distance(self, vector):
        return Vector.subtract_new(vector, self).get_magnitude()

    def copy(self):
        return Vector(self.x, self.y)

    def set(self, x, y):
        self.x = x
        self.y = y

    # TODO: THINK OF A BETTER NAME FOR THE STATIC VARIANTS
    @staticmethod
    def add_new(vector_a, vector_b):
        return Vector(vector_a.x + vector_b.x, vector_a.y + vector_b.y)

    @staticmethod
    def subtract_new(vector_a, vector_b):
        return Vector(vector_a.x - vector_b.x, vector_a.y - vector_b.y)

    @staticmethod
    def scale_new(vector, scalar):
        return Vector(vector.x * scalar, vector.y * scalar)

    @staticmethod
    def normalize_new(vector):
        return Vector.scale_new(vector, 1 / vector.get_magnitude())