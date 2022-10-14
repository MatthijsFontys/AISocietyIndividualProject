import numpy as np
from util.vector import Vector
from util.vector_pool import VectorPool
from util.util_enums import Direction as Dir


# TODO: fix it being able to zoom further than the world size
class Camera:

    def __init__(self, speed, view_width, view_height, world_width, world_height):
        self.vector_pool = VectorPool()
        self.zoom = 100
        self.interp_padding = 200
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

    def is_in_view(self, top_left, bottom_right):
        top_right = self.vector_pool.acquire(bottom_right.x, top_left.y)
        bottom_left = self.vector_pool.acquire(top_left.x, bottom_right.y)
        angles = [top_left, bottom_right, top_right, bottom_left]

        for angle in angles:
            if angle.x >= self.position.x and angle.x <= self.bottom_right.x:
                if angle.y >= self.position.y and angle.y <= self.bottom_right.y:
                    self.vector_pool.release(top_right, bottom_left)
                    return True

        self.vector_pool.release(top_right, bottom_left)
        return False

    def move(self, direction):
        self.position.add(self.movement[direction])
        self.update_bottom_right()

    def follow_position(self, player_position):
        self.position.set(player_position.x - self.view.x / 2, player_position.y - self.view.y / 2)
        self.update_bottom_right()

    def apply_zoom(self, num_to_scale):
        return num_to_scale * (self.zoom / 100)

    def set_zoom(self, zoom_in: bool, mouse_x, mouse_y):
        old_view = self.vector_pool.acquire(self.view.x, self.view.y)
        old_zoom = self.zoom
        self.zoom += self.speed
        if not zoom_in:
            self.zoom -= self.speed * 2
        min_zoom_val = min(self.default_view.x / self.world_width * 100, self.default_view.y / self.world_height * 100)
        self.zoom = np.clip(self.zoom, min_zoom_val, 200)
        self.view.scale(old_zoom / self.zoom)
        # adjusting position to the mouse x and y
        delta_mouse = self.get_delta_mouse(old_view, mouse_x, mouse_y, self.vector_pool.acquire())
        self.position.subtract(delta_mouse)
        self.update_bottom_right()
        self.vector_pool.release(old_view, delta_mouse)

    # vector needs to be the center position of the object to draw
    # should only be called after checked if the element is in camera
    def map_to_camera(self, to_map: Vector, to_set: Vector = None):
        padding = self.interp_padding
        z_padding = self.apply_zoom(padding)  # zoomed padding
        offset_pos = self.vector_pool.subtract(to_map, self.position)
        # padding is for dealing with entities that are only partially on screen
        x = np.interp(offset_pos.x, [-padding, self.view.x + padding], [-z_padding, self.default_view.x + z_padding])
        y = np.interp(offset_pos.y, [-padding, self.view.y + padding], [-z_padding, self.default_view.y + z_padding])
        self.vector_pool.release(offset_pos)
        return Vector.unpack_nullable(x, y, to_set)

    def limit_to_bounds(self):
        # todo: this limits the boundaries but not the view range when zooming
        # limit out of bounds width
        self.position.x = np.clip(self.position.x, 0, self.world_width - self.view.x)
        self.position.y = np.clip(self.position.y, 0, self.world_height - self.view.y)

    # gets the delta in mouse position after zooming
    def get_delta_mouse(self, old_view, mouse_x, mouse_y, to_set: Vector = None):
        mouse_x_world, mouse_y_world = self.get_mouse_world_pos(mouse_x, mouse_y, account_zoom=False)
        mouse_before = self.vector_pool.acquire(mouse_x_world, mouse_y_world)
        mouse_before.subtract(self.position)
        new_x = np.interp(mouse_before.x, [0, old_view.x], [0, self.view.x])
        new_y = np.interp(mouse_before.y, [0, old_view.y], [0, self.view.y])
        mouse_after = Vector.unpack_nullable(new_x, new_y, to_set)
        mouse_after.subtract(mouse_before)
        self.vector_pool.release(mouse_before)
        return mouse_after

    def get_mouse_world_pos(self, mouse_x, mouse_y, account_zoom=True):
        if account_zoom:
            mouse_x_world = np.interp(mouse_x, [0, 900], [self.position.x, self.position.x + self.view.x])
            mouse_y_world = np.interp(mouse_y, [0, 900], [self.position.y, self.position.y + self.view.y])
        else:
            mouse_x_world = np.interp(mouse_x, [0, self.default_view.x], [0, self.world_width])
            mouse_y_world = np.interp(mouse_y, [0, self.default_view.y], [0, self.world_height])

        return mouse_x_world, mouse_y_world

    def update_bottom_right(self):
        self.limit_to_bounds()
        Vector.add_new(self.position, self.view, self.bottom_right)
