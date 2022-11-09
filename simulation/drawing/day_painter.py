import pygame
from drawing.camera import Camera
from util.vector_pool import VectorPool
from world.game_tick_manager import GameTickManager
from math import floor

from world.tick_counter import TickCounter


class DayPainter:

    def __init__(self, window: pygame.Surface, camera: Camera, tick_manager: GameTickManager):
        self.tick_manager = tick_manager
        self.tick_counter = TickCounter(35, is_on=False)
        self.vector_pool = VectorPool()
        self.camera = camera
        self.window = window
        self.prev_day = self.tick_manager.day
        self.canvas = pygame.Surface((window.get_width() * 0.3, window.get_height() * 0.15), pygame.SRCALPHA)
        self.font = pygame.font.SysFont("arial", 64)

    def paint(self):
        if self.tick_manager.day > self.prev_day:
            self.tick_counter.is_on = True
            self.prev_day = self.tick_manager.day

        if self.tick_counter.is_on:
            alpha = min(320 - floor(self.tick_counter.counter / self.tick_counter.interval * 255), 255)
            self.canvas.fill(pygame.Color(67, 67, 67, alpha))
            text = self.font.render(f'Day: {self.tick_manager.day}', True, pygame.Color(255, 255, 255, alpha))
            text_rect = text.get_rect(center=self.canvas.get_rect().center)
            self.canvas.blit(text, text_rect)
            self.window.blit(self.canvas,
                             (self.window.get_width() / 2 - self.canvas.get_width() / 2,
                              self.window.get_height() - self.canvas.get_height())
                             )

    def tick(self):
        if self.tick_counter.tick():
            self.tick_counter.is_on = False
