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
        self.info_surface = pygame.Surface((window.get_width() * 0.4, window.get_height() * 0.1), pygame.SRCALPHA)
        self.font = pygame.font.SysFont("arial", 24)
        self.hunger_bar = HungerBarSprite(self.image_store, *self.info_surface.get_size())
        #self.cold_bar = ColdBarSprite(self.image_store, *self.info_surface.get_size())

    def paint(self, clicked_survivor: Survivor):
        if clicked_survivor is not None:
            self.info_surface.fill(pygame.Color(67, 67, 67, 178))
            text = self.font.render(str(f'HUNGER: {clicked_survivor.fullness}'), True, 'white')
            text_rect = text.get_rect()
            text_rect.center = self.info_surface.get_rect().center
            #self.info_surface.blit(text, text_rect)
            self.info_surface.blit(self.hunger_bar.get_image(clicked_survivor.fullness), (0, 0))
            self.window.blit(self.info_surface, (0, 0))
