import pygame
from drawing.camera import Camera
from entities.survivor import Survivor
from util.vector import Vector


class SurvivorPainter:

    def __init__(self, window, camera: Camera, population: list[Survivor]):
        self.camera = camera
        self.window = window
        self.survivor_radius = 20
        self.zoomed_survivor_radius = self.camera.apply_zoom(self.survivor_radius)
        self.population = population
        self.offset = Vector(self.zoomed_survivor_radius, self.zoomed_survivor_radius)
        self.size = Vector(self.zoomed_survivor_radius * 2, self.zoomed_survivor_radius * 2)

    def paint(self):
        self.zoomed_survivor_radius = self.camera.apply_zoom(self.survivor_radius)
        for survivor in self.population:  # AKA survivor
            l2 = Vector.subtract_new(survivor.position, self.offset)
            r2 = Vector.add_new(l2, self.size)
            if self.camera.is_in_view(l2, r2):
                offset_position = self.camera.map_to_camera(survivor.position)
                pygame.draw.circle(
                    self.window,
                    pygame.Color(58, 103, 176),
                    (offset_position.x, offset_position.y),
                    self.zoomed_survivor_radius
                )
