import pygame
from drawing.camera import Camera
from entities.survivor import Survivor
from util.vector import Vector
from ai.neuralnetwork import NeuralNetwork
from ai.layer import Layer


class NeuralNetworkPainter:

    def __init__(self, window, camera: Camera):
        self.camera = camera
        self.window = window
        self.default_radius = 40
        self.dna = NeuralNetwork(2, 4).add_layer(3).add_output_layer()
        self.origin = Vector(500, 500)

    def paint(self):
        pos = self.origin.copy()
        radius = self.camera.apply_zoom(self.default_radius)
        margin = radius * 2.5
        prev_layer_count = 0
        for i in range(len(self.dna.layers)):
            layer: Layer = self.dna.layers[i]
            pos.add(Vector(margin * 2, 0))
            pos.subtract(Vector(0, margin * prev_layer_count))
            prev_layer_count = layer.node_count
            for j in range(layer.node_count):
                v = Vector(radius / 2, radius / 2)
                l2 = Vector.subtract_new(pos, v)
                r2 = Vector.add_new(pos, v)
                if self.camera.is_in_view(l2, r2):
                    offset_position = self.camera.map_to_camera(pos)
                    pygame.draw.circle(
                        self.window,
                        pygame.Color(255, 255, 255),
                        (offset_position.x, offset_position.y),
                        radius
                    )

                pos.add(Vector(0, margin))

