from vector import Vector


class VectorPool:

    def __init__(self, size=20):
        self.pool = [Vector() for _ in range(size)]

    def acquire(self, x=0, y=0):
        vector = self.pool.pop()
        vector.set(x, y)
        return vector

    def release(self, reusable):
        self.pool.append(reusable)


