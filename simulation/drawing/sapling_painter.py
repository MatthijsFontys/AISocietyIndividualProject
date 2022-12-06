import pygame

from drawing.camera import Camera
from drawing.image_store import ImageStore
from entities.sapling import Sapling
from util.vector_pool import VectorPool


#TODO: this and campfire should be an implementation from a baseclass instead
#TODO: should make it easier to add an entity in general, and clean up code with typechecking
#TODO: still would like to add a tileset after im done this semester + animations

class SaplingPainter:
    def __init__(self, window, camera: Camera, saplings: list[Sapling]):
        self.image_store = ImageStore()
        self.vector_pool = VectorPool()
        self.camera = camera
        self.saplings = saplings
        self.window = window
        self.sapling_size = 80

    def paint(self):
        zoomed_size = self.camera.apply_zoom(self.sapling_size)
        for sapling in self.saplings:
            l2 = self.vector_pool.acquire(sapling.position.x - zoomed_size / 2, sapling.position.y - zoomed_size / 2)
            r2 = self.vector_pool.add(l2, self.vector_pool.lend(zoomed_size, zoomed_size))
            if self.camera.is_in_view(l2, r2):
                offset_position = self.camera.map_to_camera(sapling.position, self.vector_pool.acquire())
                self.window.blit(sapling.get_sprite(self).get_image(zoomed_size),
                                 (offset_position.x, offset_position.y)
                                 )
                self.vector_pool.release(offset_position)
            self.vector_pool.release(l2, r2)


