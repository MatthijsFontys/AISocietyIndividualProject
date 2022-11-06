from glob import glob
import pygame.sprite


class StatBarBase(pygame.sprite.Sprite):

    def __init__(self, image_store, width, glob_pattern):
        super(StatBarBase, self).__init__()
        self.image_store = image_store
        self.value = 100
        self.images = [self.load_image(x) for x in glob(glob_pattern)]
        self.aspect_ratio = self.images[0].get_width() / self.images[0].get_height()
        self.width = width * 0.75
        self.height = self.width / self.aspect_ratio

    def load_image(self, filename):
        image = self.image_store.get(filename)
        if image is None:
            image = pygame.image.load(filename).convert_alpha()
            self.image_store.update({filename: image})
        return image

    def get_image(self, value):
        size = (self.width, (self.width / self.aspect_ratio))
        fill = pygame.transform.scale(self.images[0], size)
        outline = pygame.transform.scale(self.images[1], size)
        canvas = pygame.Surface(size).convert_alpha()
        canvas.fill(pygame.Color(0, 0, 0, 0))
        canvas.blit(fill, (0, 0), area=(0, 0, self.width * (value / 100), fill.get_height()))
        canvas.blit(outline, (0, 0))
        return canvas

