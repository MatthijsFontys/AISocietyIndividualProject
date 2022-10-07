import pygame
from drawing.camera import Camera
from drawing.sprites.survivor_sprite import SurvivorSprite
from entities.survivor import Survivor
from util.vector import Vector
from util.vector_pool import VectorPool


class SurvivorPainter:

    def __init__(self, window, camera: Camera, population: list[Survivor]):
        self.vector_pool = VectorPool()
        self.camera = camera
        self.window = window
        self.survivor_radius = 20
        self.zoomed_survivor_radius = self.camera.apply_zoom(self.survivor_radius)
        self.population = population
        self.offset = Vector(self.zoomed_survivor_radius, self.zoomed_survivor_radius)
        self.size = Vector(self.zoomed_survivor_radius * 2, self.zoomed_survivor_radius * 2)

        self.spr = SurvivorSprite()

    def paint(self):
        self.zoomed_survivor_radius = self.camera.apply_zoom(self.survivor_radius)
        for survivor in self.population:  # AKA survivor
            l2 = self.vector_pool.subtract(survivor.position, self.offset)
            r2 = self.vector_pool.add(l2, self.size)
            if self.camera.is_in_view(l2, r2):
                offset_position = self.camera.map_to_camera(survivor.position, self.vector_pool.acquire())
                # pygame.draw.circle(
                #     self.window,
                #     pygame.Color(58, 103, 176),
                #     (offset_position.x, offset_position.y),
                #     self.zoomed_survivor_radius
                # )
                self.window.blit(self.spr.get_image(self.zoomed_survivor_radius * 2.5), (offset_position.x, offset_position.y))
                self.spr.update()
                self.vector_pool.release(offset_position)
            self.vector_pool.release(l2, r2)
