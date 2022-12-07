from drawing.camera import Camera
from drawing.image_store import ImageStore
from util.vector_pool import VectorPool
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.entity_base import EntityBase


class EntityPainter:

    def __init__(self, window, camera: Camera, entities: list['EntityBase'], entity_size):
        self.image_store = ImageStore()
        self.vector_pool = VectorPool()
        self.camera = camera
        self.entities = entities
        self.window = window
        self.entity_size = entity_size

    def paint(self):
        zoomed_size = self.camera.apply_zoom(self.entity_size)
        for entity in self.entities:
            l2 = self.vector_pool.acquire(entity.position.x - zoomed_size / 2, entity.position.y - zoomed_size / 2)
            r2 = self.vector_pool.add(l2, self.vector_pool.lend(zoomed_size, zoomed_size))
            if self.camera.is_in_view(l2, r2):
                offset_position = self.camera.map_to_camera(entity.position, self.vector_pool.acquire())
                self.window.blit(entity.get_sprite(self).get_image(zoomed_size),
                                 (offset_position.x, offset_position.y)
                                 )

                self.vector_pool.release(offset_position)
            self.vector_pool.release(l2, r2)
