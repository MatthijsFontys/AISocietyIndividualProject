import pygame
from drawing.camera import Camera
from util.vector_pool import VectorPool
from world.time.game_tick_dto import GameTickDto
from math import floor
from world.time.tick_counter import TickCounter
from util.linalg import lerp


class DayPainter:

    # Todo: make a store for the fonts

    def __init__(self, window: pygame.Surface, camera: Camera, tick_dto: GameTickDto):
        self.MINUTES_IN_DAY = 1440  # 60 * 24
        self.tick_dto = tick_dto
        self.tick_counter = TickCounter(35, is_on=False)
        self.vector_pool = VectorPool()
        self.camera = camera
        self.window = window
        self.notify_canvas = pygame.Surface((window.get_width() * 0.3, window.get_height() * 0.15), pygame.SRCALPHA)
        self.font = pygame.font.SysFont("arial", 64)
        self.small_font = pygame.font.Font("drawing/assets/fonts/dpcomic.ttf", 32)
        self.notify_y = self.window.get_height() - self.notify_canvas.get_height()



    def paint(self):

        # Time of day transparent overlay
        overlay = pygame.Surface(self.window.get_size(), pygame.SRCALPHA)

        night_clr = pygame.Color(7, 34, 93, 151)  # '#07225D'
        day_clr = pygame.Color(214, 196, 185, 42)  # '#D6C4B9'
        day_percent = self.tick_dto.get_day_percent()
        if day_percent < 0.5:
            lerped_clr = night_clr.lerp(day_clr, day_percent / 0.5)
        else:
            lerped_clr = day_clr.lerp(night_clr, (day_percent-0.5) / 0.5)
        overlay.fill(lerped_clr)
        self.window.blit(overlay, (0, 0))

        # Current time and day
        minutes = day_percent * self.MINUTES_IN_DAY
        hours = floor(minutes / 60)
        minutes = floor(minutes - hours * 60)
        min_prefix = '0' if minutes < 10 else ''
        prefix = 'AM' if hours < 12 else 'PM'
        if hours == 0:
            hours += 12
        else:
            hours = hours - 12 if hours > 12 else hours
        text = self.small_font.render(f'Day {self.tick_dto.day}', True, pygame.Color(255, 255, 255))
        time_text = self.small_font.render(f'{hours}:{min_prefix}{minutes} {prefix}', True, pygame.Color(255, 255, 255))
        time_canvas = pygame.Surface((self.window.get_width() * 0.15, self.window.get_height() * 0.2), pygame.SRCALPHA)
        time_canvas.blit(text, (text.get_rect(center=time_canvas.get_rect().center).x, 20))
        time_canvas.blit(time_text, (time_text.get_rect(center=time_canvas.get_rect().center).x, 28 + time_text.get_height()))
        self.window.blit(time_canvas, (self.window.get_width() - time_canvas.get_width(), 0))

        # New day announcement
        if self.tick_counter.is_on:
            text = self.font.render(f'Day {self.tick_dto.day}', True, pygame.Color(255, 255, 255))
            text_rect = text.get_rect(center=self.notify_canvas.get_rect().center)
            self.notify_canvas.fill(pygame.Color(67, 67, 67))
            self.notify_canvas.blit(text, text_rect)
            if self.tick_counter.get_percentage() > 0.5:
                self.notify_y += max(lerp(self.notify_y, self.window.get_height(), 0.015) - self.notify_y, 0.5)
            self.window.blit(self.notify_canvas,
                             (self.window.get_width() / 2 - self.notify_canvas.get_width() / 2,
                              self.notify_y)
                             )

    def tick(self, new_day):
        if new_day:
            self.tick_counter.is_on = True
            self.notify_y = self.window.get_height() - self.notify_canvas.get_height()
        elif self.tick_counter.tick():
            self.tick_counter.is_on = False
