from vector import Vector


class VectorPool:

    def __init__(self, size):
        self.pool = [Vector() for _ in range(size)]

    def acquire(self):
        return self.pool.pop()

    def release(self, reusable):
        self.pool.append(reusable)


