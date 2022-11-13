from util.vector import Vector


def lerp(x, y, a):
    return x * (1 - a) + y * a


def lerp_vec(va, vb, a, to_set: Vector = None):
    return Vector.unpack_nullable(lerp(va.x, vb.x, a), lerp(va.y, vb.y, a), to_set)


def sine(a):
    return 1 if a > 0 else -1
