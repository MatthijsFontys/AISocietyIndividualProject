from vector import Vector
from my_enums import Direction as Dir


class Camera:

    def __init__(self, speed, view_width, view_height, world_width, world_height):
        self.zoom = 100
        self.position = Vector(0, 0)  # aka top left
        self.view = Vector(view_width, view_height)
        self.bottom_right = Vector.add_new(self.position, self.view)
        self.world_width = world_width
        self.world_height = world_height
        self.speed = speed
        self.movement = {
            Dir.UP: Vector(0, -speed),
            Dir.DOWN: Vector(0, speed),
            Dir.LEFT: Vector(-speed, 0),
            Dir.RIGHT: Vector(speed, 0)
        }

    def is_in_view(self, l2, r2):
        # algorithm from https://www.geeksforgeeks.org/find-two-rectangles-overlap/
        # l1 = top left coordinate of camera
        # r1 = bottom right coordinate of camera
        # l2 is top left of object to check
        # r2 is bottom right of object to check
        l1 = self.position
        r1 = self.bottom_right

        to_return = False

        # if one rectangle is within the other rectangle
        if (l2.x > l1.x and l2.y > l1.y) and (r2.x < r1.x and r2.y < r1.y):
            to_return = True
        # if rectangle has area 0, no overlap
        elif l1.x == r1.x or l1.y == r1.y or r2.x == l2.x or l2.y == r2.y:
            to_return = False

        # If one rectangle is on left side of other
        elif l1.x > r2.x or l2.x > r1.x:
            to_return = False

        # If one rectangle is above other
        elif r1.y > l2.y or r2.y > l1.y:
            to_return = False

        return to_return

    def move(self, direction):
        self.position.add(self.movement[direction])

        # limit out of bounds width
        self.position.x = min(self.position.x, self.world_width - self.view.x)
        self.position.x = max(self.position.x, 0)

        # limit out of bounds height
        self.position.y = min(self.position.y, self.world_height - self.view.y)
        self.position.y = max(self.position.y, 0)

        # calc new bottom right after movement
        self.bottom_right = Vector.add_new(self.position, self.view)

    def apply_zoom(self, num_to_scale):
        return num_to_scale * (self.zoom / 100)

    def set_zoom(self, delta_zoom):
        # TODO: FIGURE OUT WHERE I AM GOING WRONG
        old_zoom = self.zoom
        self.zoom += delta_zoom
        self.zoom = min(self.zoom, 200)
        self.zoom = max(self.zoom, 50)

        self.view.scale(self.zoom / old_zoom)
        self.bottom_right = Vector.add_new(self.position, self.view)

