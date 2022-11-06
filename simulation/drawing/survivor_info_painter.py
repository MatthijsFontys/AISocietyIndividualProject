import pygame
from drawing.camera import Camera
from math import floor

from drawing.sprites.cold_bar_sprite import ColdBarSprite
from drawing.sprites.hunger_bar_sprite import HungerBarSprite
from drawing.sprites.survivor_sprite import SurvivorSprite
from entities.survivor import Survivor
from util.vector import Vector
from util.vector_pool import VectorPool


class SurvivorInfoPainter:

    def __init__(self, window: pygame.Surface, camera: Camera):
        self.image_store = {}
        self.vector_pool = VectorPool()
        self.camera = camera
        self.window = window
        self.info_surface = pygame.Surface((window.get_width() * 0.4, window.get_height() * 0.3), pygame.SRCALPHA)
        self.font = pygame.font.SysFont("arial", 24)
        self.padding = 20
        self.start_y = self.padding
        self.hunger_bar = HungerBarSprite(self.image_store, self.info_surface.get_width())
        self.cold_bar = ColdBarSprite(self.image_store, self.info_surface.get_width())

    def paint(self, clicked_survivor: Survivor):
        if clicked_survivor is not None:
            self.start_y = self.padding

            self.info_surface.fill(pygame.Color(67, 67, 67, 178))
            w, h = self.info_surface.get_size()

            # Age
            age_text = self.font.render(f'AGE: 42 days', True, 'white')
            self.info_surface.blit(age_text, (self.padding, self.start_y))
            self.start_y += self.font.get_linesize() + self.padding

            # Hunger bar
            self.draw_stat_bar(self.hunger_bar, 'HUNGER:', clicked_survivor.fullness, w)
            # Cold bar
            self.draw_stat_bar(self.cold_bar, 'COLD:', 100, w)

            # Blit surface holding all the info
            self.window.blit(self.info_surface, (0, 0))

    def draw_stat_bar(self, bar, text, value, w):
        text = self.font.render(text, True, 'white')
        self.info_surface.blit(text, (self.padding, self.start_y))
        self.start_y += self.font.get_linesize()
        self.info_surface.blit(bar.get_image(value), (w*0.125, self.start_y))
        self.start_y += bar.height + self.padding

