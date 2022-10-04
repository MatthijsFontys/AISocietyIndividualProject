from util.vector import Vector


class VectorPool:

    def __init__(self, size=5):
        self.pool = [Vector() for _ in range(size)]

    def acquire(self, x=0, y=0):
        vector = self.pool.pop()
        vector.set(x, y)
        return vector

    def release(self, *reusable):
        for vector in reusable:
            self.pool.append(vector)

    # Get vector that would be released immediately
    def lend(self, x=0, y=0):
        self.pool[0].set(x, y)
        return self.pool[0]

    # Methods for vector calculations with the result in a new acquired vector
    def add(self, vector_a, vector_b):
        return Vector.add_new(vector_a, vector_b, self.acquire())

    def subtract(self, vector_a, vector_b):
        return Vector.subtract_new(vector_a, vector_b, self.acquire())

    def scale(self, vector, scalar):
        return Vector.scale_new(vector, scalar, self.acquire())

    def normalize(self, vector):
        return Vector.normalize_new(vector, self.acquire())
