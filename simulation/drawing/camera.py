from util.vector import Vector
from util.util_enums import Direction as Dir


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
        # TODO: SOMETHING IS WRONG WITH MY OLD METHOD, SOME TIMES THINGS DISAPPEAR FROM SCREEN WHEN THEY ARE STILL PARTIALLY VISIBLE
        # TODO: IF THIS NEW METHOD IS TOO SLOW GO BACK TO THE OLD METHOD AND FIX IT INSTEAD
        # TODO: might use object pooling if using so many vectors slows down the program
        # algorithm from https://www.geeksforgeeks.org/find-two-rectangles-overlap/
        # l1 = top left coordinate of camera
        # r1 = bottom right coordinate of camera
        # l2 is top left of object to check
        # r2 is bottom right of object to check
        l1 = self.position
        r1 = self.bottom_right

        angles = [l2, r2, Vector(r2.x, l2.y), Vector(l2.x, r2.y)]

        for angle in angles:
            if angle.x >= self.position.x and angle.x <= self.bottom_right.x:
                if angle.y >= self.position.y and angle.y <= self.bottom_right.y:
                    return True

        return False

    def move(self, direction):
        self.position.add(self.movement[direction])

        self.limit_to_bounds()
        # calc new bottom right after movement
        self.bottom_right = Vector.add_new(self.position, self.view)

    def follow_player(self, player_position):
        self.position = Vector(player_position.x - self.view.x / 2, player_position.y - self.view.y / 2)
        self.limit_to_bounds()
        self.bottom_right = Vector.add_new(self.position, self.view)

    def apply_zoom(self, num_to_scale):
        #return num_to_scale
        return num_to_scale * (self.zoom / 100)

    def set_zoom(self, delta_zoom):
        # TODO: FIGURE OUT HOW TO ADJUST THE OFFSET FOR THE OBJECTS WITHIN VIEW
        old_zoom = self.zoom
        self.zoom += delta_zoom
        if self.zoom < 20:
            self.zoom = 20
        elif self.zoom > 200:
            self.zoom = 200
        #
        # self.position.scale(- (self.zoom / old_zoom / 2))
        # self.limit_to_bounds()
        self.view.scale(2.1 - self.zoom / old_zoom / 2)
        self.bottom_right = Vector.add_new(self.position, self.view)
        pass

    def limit_to_bounds(self):
        # limit out of bounds width
        self.position.x = min(self.position.x, self.world_width - self.view.x)
        self.position.x = max(self.position.x, 0)

        # limit out of bounds height
        self.position.y = min(self.position.y, self.world_height - self.view.y)
        self.position.y = max(self.position.y, 0)

