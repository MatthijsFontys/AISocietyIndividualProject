import pygame
from drawing.camera import Camera
from util.vector_pool import VectorPool
from world.game_tick_manager import GameTickManager


class DayPainter:

    def __init__(self, window: pygame.Surface, camera: Camera, tick_manager: GameTickManager):
        self.tick_manager = tick_manager
        self.vector_pool = VectorPool()
        self.camera = camera
        self.window = window
        self.prev_day = self.tick_manager.day
        self.canvas = pygame.Surface((window.get_width() * 0.3, window.get_height() * 0.15), pygame.SRCALPHA)
        self.timer = 0
        self.font = pygame.font.SysFont("arial", 64)
        self.timer_threshold = 50

    def paint(self):
        if self.tick_manager.day > self.prev_day or self.timer < self.timer_threshold:
            self.canvas.fill(pygame.Color(67, 67, 67, 178))
            text = self.font.render(f'Day: {self.tick_manager.day}', True, 'white')
            text_rect = text.get_rect(center=self.canvas.get_rect().center)
            self.canvas.blit(text, text_rect)
            self.window.blit(self.canvas,
                             (self.window.get_width() / 2 - self.canvas.get_width() / 2,
                              self.window.get_height() - self.canvas.get_height())
                             )
            self.timer += 1
            self.prev_day = self.tick_manager.day
            if self.timer >= self.timer_threshold:
                self.timer = 0



