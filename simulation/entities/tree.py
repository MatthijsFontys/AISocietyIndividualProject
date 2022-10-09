from drawing.sprites.tree_sprite import TreeSprite
from util.vector_pool import VectorPool

class Tree:

    def __init__(self, position):
        self.vector_pool = VectorPool()
        self.food_count = 3
        self.max_food_count = 3
        self.ticks_since_grow = 0
        self.forage_tick_cooldown = 20
        self.ticks_since_forage = self.forage_tick_cooldown
        self.forage_range = 80
        self.position = position
        self.sprite = None

    def try_forage_food(self, survivor):
        is_in_range = self.position.get_distance_squared(survivor.position, self.vector_pool.lend()) <= self.forage_range ** 2
        is_off_cooldown = self.ticks_since_forage >= self.forage_tick_cooldown
        if self.food_count > 0 and is_in_range and is_off_cooldown:
            self.update_food_count(-1)
            survivor.give_food()
            self.ticks_since_forage = 0
            return True
        return False

    def tick(self):
        self.ticks_since_forage += 1
        self.ticks_since_grow += 1
        if self.ticks_since_grow > 30:
            if self.food_count < self.max_food_count:
                self.update_food_count(1)
            self.ticks_since_grow = 0

    def get_sprite(self, tree_painter):
        if self.sprite is None:
            self.sprite = TreeSprite(tree_painter.image_store)
        return self.sprite

    def update_food_count(self, delta_food):
        self.food_count += delta_food
        if self.sprite is not None:
            self.sprite.notify(self)

