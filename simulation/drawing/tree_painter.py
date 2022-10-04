import pygame
import math
from util.vector_pool import VectorPool
from drawing.camera import Camera
from entities.tree import Tree


class TreePainter:

    def __init__(self, window, camera: Camera, trees: list[Tree]):
        self.vector_pool = VectorPool()
        self.camera = camera
        self.trees = trees
        self.window = window

    def paint(self, survivor_radius, show_range=True, show_fruit_count=True):
        draw_counter = 0  # TODO: remove temp variable used for debugging the camera | or move the variable to the camera instead idk
        tree_size = self.camera.apply_zoom(80)

        for tree in self.trees:  # AKA tree
            l2 = self.vector_pool.acquire(tree.position.x - tree_size / 2, tree.position.y - tree_size / 2)
            r2 = self.vector_pool.add(l2, self.vector_pool.lend(tree_size, tree_size))
            if self.camera.is_in_view(l2, r2):
                draw_counter += 1
                offset_position = self.camera.map_to_camera(tree.position, self.vector_pool.acquire())
                offset_x = offset_position.x - tree_size / 2
                offset_y = offset_position.y - tree_size / 2
                tree_rect = pygame.Rect(offset_x, offset_y, tree_size, tree_size)

                # TODO: Fix it so it doesnt have to calculate the range size for every tree in the loop
                if show_range:
                    range_size = self.camera.apply_zoom(tree.forage_range - survivor_radius)
                    pygame.draw.circle(self.window, pygame.Color(148, 22, 37), (offset_position.x, offset_position.y), range_size)

                pygame.draw.rect(self.window, pygame.Color(13, 56, 13), tree_rect)

                if show_fruit_count:
                    main_font = pygame.font.SysFont("arial", math.floor(self.camera.apply_zoom(48)))
                    text = main_font.render(str(tree.food_count), True, 'white')
                    text_rect = text.get_rect()
                    text_rect.center = tree_rect.center
                    self.window.blit(text, text_rect)
                self.vector_pool.release(offset_position)
            self.vector_pool.release(l2, r2)
