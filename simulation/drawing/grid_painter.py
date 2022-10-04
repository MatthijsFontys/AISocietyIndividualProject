import pygame
import math
from drawing.camera import Camera
from world.collision_grid import CollisionGrid
from util.vector_pool import VectorPool


class GridPainter:

    def __init__(self, window, camera: Camera, grid: CollisionGrid):
        self.vector_pool = VectorPool()
        self.camera = camera
        self.window = window
        self.grid = grid

    def paint(self, should_paint=True, draw_index=False):
        if should_paint:
            # GRID
            size = self.camera.apply_zoom(self.grid.cell_size)
            for i in range(self.grid.width):
                for j in range(self.grid.height):
                    x = i * self.grid.cell_size
                    y = j * self.grid.cell_size
                    pos = self.vector_pool.acquire(x, y)
                    if self.camera.is_in_view(pos, self.vector_pool.lend(x + size, y + size)):
                        pos = self.camera.map_to_camera(pos, pos)
                        grid_rect = pygame.Rect(pos.x, pos.y, size, size)
                        pygame.draw.rect(self.window, pygame.Color(255, 255, 255), grid_rect, 1)

                        # todo: Make a class for drawing, because I can't keep creating this font every time (DRY)
                        # drawing grid index for debugging
                        if draw_index:
                            main_font = pygame.font.SysFont("arial", math.floor(self.camera.apply_zoom(48)))
                            text = main_font.render(str(i + j * self.grid.width), True, 'white')
                            text_rect = text.get_rect()
                            text_rect.center = grid_rect.center
                            self.window.blit(text, text_rect)
                    self.vector_pool.release(pos)
