import pygame
from drawing.camera import Camera
from world.collision_grid import CollisionGrid
from util.vector import Vector


class GridPainter:

    def __init__(self, window, camera: Camera, grid: CollisionGrid):
        self.camera = camera
        self.window = window
        self.grid = grid

    # TODO: FIX THE GRID WITH THE ZOOMING CAMERA!
    def paint(self, should_paint=True):
        if should_paint:
            # GRID
            size = self.camera.apply_zoom(self.grid.cell_size)
            for i in range(self.grid.width):
                for j in range(self.grid.height):
                    x = i * size
                    y = j * size
                    pos = Vector(x, y)
                    if self.camera.is_in_view(pos, Vector(x + size, y + size)) and self.camera.zoom == 100:
                        offset_position = Vector.subtract_new(pos, self.camera.position) #self.camera.map_to_camera(Vector(x, y))
                        grid_rect = pygame.Rect(offset_position.x, offset_position.y, size, size)
                        pygame.draw.rect(self.window, pygame.Color(255, 255, 255), grid_rect, 1)
