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

    def get_distance(self, vector, to_set=None):
        return Vector.subtract_new(vector, self, to_set).get_magnitude()

    def get_distance_squared(self, vector, to_set=None):
        dist = Vector.subtract_new(vector, self, to_set)
        a_squared = dist.x ** 2
        b_squared = dist.y ** 2
        return a_squared + b_squared

    def equals(self, vector):
        return self.x == vector.x and self.y == vector.y

    def copy(self):
        return Vector(self.x, self.y)

    def set(self, x, y):
        self.x = x
        self.y = y

    # TODO: THINK OF A BETTER NAME FOR THE STATIC VARIANTS
    @staticmethod
    def unpack_nullable(x=0, y=0, to_set=None):
        unpacked = to_set or Vector()
        unpacked.set(x, y)
        return unpacked

    # To be used with the vector pool, to reduce creation of new vectors every frame
    @staticmethod
    def add_new(vector_a, vector_b, to_set=None):
        to_set = Vector.unpack_nullable(to_set=to_set)
        to_set.set(vector_a.x + vector_b.x, vector_a.y + vector_b.y)
        return to_set

    @staticmethod
    def subtract_new(vector_a, vector_b, to_set=None):
        to_set = Vector.unpack_nullable(to_set=to_set)
        to_set.set(vector_a.x - vector_b.x, vector_a.y - vector_b.y)
        return to_set

    @staticmethod
    def scale_new(vector, scalar, to_set=None):
        to_set = Vector.unpack_nullable(to_set=to_set)
        to_set.set(vector.x * scalar, vector.y * scalar)
        return to_set

    @staticmethod
    def normalize_new(vector, to_set=None):
        to_set = Vector.unpack_nullable(to_set=to_set)
        Vector.scale_new(vector, 1 / vector.get_magnitude(), to_set)
        return to_set
