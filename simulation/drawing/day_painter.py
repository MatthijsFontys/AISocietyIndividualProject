import pygame
import numpy as np
from drawing.camera import Camera
from util.vector_pool import VectorPool
from world.game_tick_dto import GameTickDto
from world.game_tick_manager import GameTickManager
from math import floor

from world.tick_counter import TickCounter


class DayPainter:

    def __init__(self, window: pygame.Surface, camera: Camera, tick_dto: GameTickDto):
        self.tick_dto = tick_dto
        self.tick_counter = TickCounter(35, is_on=False)
        self.vector_pool = VectorPool()
        self.camera = camera
        self.window = window
        self.canvas = pygame.Surface((window.get_width() * 0.3, window.get_height() * 0.15), pygame.SRCALPHA)
        self.font = pygame.font.SysFont("arial", 64)

    def paint(self):
        if self.tick_counter.is_on:
            self.canvas.fill(pygame.Color(67, 67, 67))
            text = self.font.render(f'Day: {self.tick_dto.day}', True, pygame.Color(255, 255, 255))
            text_rect = text.get_rect(center=self.canvas.get_rect().center)
            self.canvas.blit(text, text_rect)
            self.window.blit(self.canvas,
                             (self.window.get_width() / 2 - self.canvas.get_width() / 2,
                              self.window.get_height() - self.canvas.get_height())
                             )

    def tick(self, new_day):
        if new_day:
            self.tick_counter.is_on = True
        elif self.tick_counter.tick():
            self.tick_counter.is_on = False
