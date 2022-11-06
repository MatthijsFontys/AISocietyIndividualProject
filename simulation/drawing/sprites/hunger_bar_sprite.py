from glob import glob
import pygame.sprite


class HungerBarSprite(pygame.sprite.Sprite):

    def __init__(self, image_store, width, height):
        super(HungerBarSprite, self).__init__()
        self.image_store = image_store
        self.value = 100
        self.width = width
        self.height = height
        self.images = [self.load_image(x) for x in glob("assets/cold_bar*.svg")]

    def load_image(self, filename):
        image = self.image_store.get(filename)
        if image is None:
            image = pygame.image.load(filename).convert_alpha()
            self.image_store.update({filename: image})
        return image

    def get_image(self, value):
        fill = pygame.transform.scale(self.images[0], (self.width * 3, (self.width / 4.336) * 3))
        # fill = fill.subsurface((0, 0, self.width * 3 * (value / 100), (self.width / 4.336) * 3))
        outline = pygame.transform.scale(self.images[1], (self.width * 3, (self.width / 4.336) * 3))
        canvas = pygame.Surface(outline.get_size()).convert_alpha()
        canvas.fill(pygame.Color(0, 0, 0, 0))
        pygame.transform.scale(canvas, (100, 23))
        #print(fill.get_width())
        canvas.blit(fill, (0, 0), area=(0, 0, 300 * (value / 100), fill.get_height()))
        canvas.blit(outline, (0, 0))
        return canvas

