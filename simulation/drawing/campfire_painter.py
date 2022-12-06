import pygame

from drawing.camera import Camera
from drawing.image_store import ImageStore
from entities.campfire import Campfire
from util.vector_pool import VectorPool


class CampfirePainter:
    def __init__(self, window, camera: Camera, fires: list[Campfire]):
        self.image_store = ImageStore()
        self.vector_pool = VectorPool()
        self.camera = camera
        self.fires = fires
        self.window = window
        self.fire_size = 160

    def paint(self):
        zoomed_size = self.camera.apply_zoom(self.fire_size)
        for fire in self.fires:
            l2 = self.vector_pool.acquire(fire.position.x - zoomed_size / 2, fire.position.y - zoomed_size / 2)
            r2 = self.vector_pool.add(l2, self.vector_pool.lend(zoomed_size, zoomed_size))
            if self.camera.is_in_view(l2, r2):
                offset_position = self.camera.map_to_camera(fire.position, self.vector_pool.acquire())
                self.window.blit(fire.get_sprite(self).get_image(zoomed_size),
                                 (offset_position.x, offset_position.y)
                                 )

                self.vector_pool.release(offset_position)
            self.vector_pool.release(l2, r2)
