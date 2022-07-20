import pygame
from drawing.camera import Camera
from world.collision_grid import CollisionGrid
from util.vector import Vector


class GridPainter:

    def __init__(self, window, camera: Camera, grid: CollisionGrid):
        self.camera = camera
        self.window = window
        self.grid = grid

    # TODO: FIGURE OUT WHY CELLS ARE NOT GETTING PAINTED WHEN THEY ARE NOT ENTIRELY WITHIN THE CAMERA
    def paint(self, should_paint=True):
        if should_paint:
            # GRID
            size = self.camera.apply_zoom(self.grid.cell_size)
            for i in range(self.grid.width):
                for j in range(self.grid.height):
                    x = i * size
                    y = j * size
                    if self.camera.is_in_view(Vector(x, y), Vector(x + size, y + size)):
                        offset_position = self.camera.map_to_camera(Vector(x, y))
                        grid_rect = pygame.Rect(offset_position.x, offset_position.y, size, size)
                        pygame.draw.rect(self.window, pygame.Color(255, 255, 255), grid_rect, 1)
