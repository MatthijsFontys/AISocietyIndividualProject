import pygame

from drawing.grid_painter import GridPainter
from drawing.survivor_painter import SurvivorPainter
from drawing.tree_painter import TreePainter
from world.overworld_map import OverworldMap
from drawing.camera import Camera


class DrawFactory:

    def __init__(self, window: pygame.Surface, world: OverworldMap):
        self.MAP = world
        self.WINDOW = window
        self.MOUSE_SPEED = 10
        self.camera = Camera(self.MOUSE_SPEED, window.get_width(), window.get_height(), world.WIDTH, world.HEIGHT)

        self.grid_painter = GridPainter(self.WINDOW, self.camera, self.MAP.collision_grid)
        self.survivor_painter = SurvivorPainter(self.WINDOW, self.camera, self.MAP.population)
        self.tree_painter = TreePainter(self.WINDOW, self.camera, self.MAP.trees)

