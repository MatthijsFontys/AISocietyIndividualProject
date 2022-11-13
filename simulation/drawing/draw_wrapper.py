import pygame

from drawing.day_painter import DayPainter
from drawing.grid_painter import GridPainter
from drawing.survivor_info_painter import SurvivorInfoPainter
from drawing.survivor_painter import SurvivorPainter
from drawing.tree_painter import TreePainter
from world.time.game_tick_manager import GameTickManager
from world.map.overworld_map import OverworldMap
from drawing.camera import Camera


class DrawWrapper:

    def __init__(self, window: pygame.Surface, world: OverworldMap, tick_manager: GameTickManager):
        self.tick_manager = tick_manager
        self.MAP = world
        self.WINDOW = window
        self.MOUSE_SPEED = 10
        self.camera = Camera(self.MOUSE_SPEED, window.get_width(), window.get_height(), world.WIDTH, world.HEIGHT)

        self.grid_painter = GridPainter(self.WINDOW, self.camera, self.MAP.collision_grid)
        self.survivor_painter = SurvivorPainter(self.WINDOW, self.camera, self.MAP.population)
        self.tree_painter = TreePainter(self.WINDOW, self.camera, self.MAP.trees)

        self.survivor_info_painter = SurvivorInfoPainter(self.WINDOW, self.camera, self.tick_manager)
        self.day_painter = DayPainter(self.WINDOW, self.camera, self.tick_manager.dto)

