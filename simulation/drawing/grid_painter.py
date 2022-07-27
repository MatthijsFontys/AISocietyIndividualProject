import pygame
import math
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
        if should_paint and self.camera.zoom == 100:
            # GRID
            size = self.camera.apply_zoom(self.grid.cell_size)
            half_size = Vector(size / 2, size / 2)
            for i in range(self.grid.width):
                for j in range(self.grid.height):
                    x = i * size
                    y = j * size
                    pos = Vector(x, y)
                    if self.camera.is_in_view(pos, Vector(x + size, y + size)):
                        pos.add(half_size)
                        # The map to camera method needs a center position
                        offset_position = self.camera.map_to_camera(pos)
                        offset_position.subtract(half_size)
                        grid_rect = pygame.Rect(offset_position.x, offset_position.y, size, size)
                        pygame.draw.rect(self.window, pygame.Color(255, 255, 255), grid_rect, 1)

                        # todo: Make a class for drawing, because I can't keep creating this font every time (DRY)
                        # drawing grid index for debugging
                        # main_font = pygame.font.SysFont("arial", math.floor(self.camera.apply_zoom(48)))
                        # text = main_font.render(str(i + j * self.grid.width), True, 'white')
                        # text_rect = text.get_rect()
                        # text_rect.center = grid_rect.center
                        # self.window.blit(text, text_rect)
