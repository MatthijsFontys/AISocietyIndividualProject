import numpy as np
from util.vector import Vector
from util.util_enums import Direction as Dir


class Camera:

    def __init__(self, speed, view_width, view_height, world_width, world_height):
        self.zoom = 100
        self.interp_padding = 80
        self.position = Vector(0, 0)  # aka top left
        self.view = Vector(view_width, view_height)
        self.default_view = Vector(view_width, view_height)
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
        angles = [l2, r2, Vector(r2.x, l2.y), Vector(l2.x, r2.y)]

        for angle in angles:
            if angle.x >= self.position.x and angle.x <= self.bottom_right.x:
                if angle.y >= self.position.y and angle.y <= self.bottom_right.y:
                    return True

        return False

    def move(self, direction):
        self.position.add(self.movement[direction])
        self.limit_to_bounds()
        self.bottom_right = Vector.add_new(self.position, self.view)

    def follow_player(self, player_position):
        self.position = Vector(player_position.x - self.view.x / 2, player_position.y - self.view.y / 2)
        self.limit_to_bounds()
        self.bottom_right = Vector.add_new(self.position, self.view)

    def apply_zoom(self, num_to_scale):
        return num_to_scale * (self.zoom / 100)

    def set_zoom(self, zoom_in: bool, mouse_x, mouse_y):
        old_view = Vector(self.view.x, self.view.y)
        old_zoom = self.zoom
        self.zoom += self.speed
        if not zoom_in:
            self.zoom -= self.speed * 2
        self.zoom = np.clip(self.zoom, 55, 200)
        self.view.scale(old_zoom / self.zoom)
        # adjusting position to the mouse x and y
        mouse_x_world = np.interp(mouse_x, [0, self.default_view.x], [0, self.world_width])
        mouse_y_world = np.interp(mouse_y, [0, self.default_view.y], [0, self.world_height])
        mouse_before = Vector(mouse_x_world, mouse_y_world)
        mouse_before.subtract(self.position)
        new_x = np.interp(mouse_before.x, [0, old_view.x], [0, self.view.x])
        new_y = np.interp(mouse_before.y, [0, old_view.y], [0, self.view.y])
        mouse_after = Vector(new_x, new_y)
        mouse_after.subtract(mouse_before)
        self.position.subtract(mouse_after)
        self.limit_to_bounds()
        self.bottom_right = Vector.add_new(self.position, self.view)

    def map_to_camera(self, to_map: Vector):
        size = self.interp_padding
        zoomed_size = self.apply_zoom(size)
        offset_pos = Vector.subtract_new(to_map, self.position)
        x = np.interp(offset_pos.x, [-size, self.view.x + size], [-zoomed_size, self.default_view.x + zoomed_size])
        y = np.interp(offset_pos.y, [-size, self.view.y + size], [-zoomed_size, self.default_view.y + zoomed_size])
        return Vector(x, y)

    def limit_to_bounds(self):
        # todo: this limits the boundaries but not the view range when zooming
        # limit out of bounds width
        self.position.x = min(self.position.x, self.world_width - self.view.x)
        self.position.x = max(self.position.x, 0)

        # limit out of bounds height
        self.position.y = min(self.position.y, self.world_height - self.view.y)
        self.position.y = max(self.position.y, 0)
