class Tree:

    def __init__(self, position):
        self.food_count = 3
        self.ticks_since_grow = 0
        self.forage_range = 50
        # Need something to keep track of when to regrow food
        self.position = position

    def try_forage_food(self, survivor):
        if self.food_count > 0 and self.position.get_distance(survivor.position) <= self.forage_range:
            self.food_count -= 1
            survivor.give_food()
            return True
        return False

    def try_grow_food(self):
        self.ticks_since_grow += 1
        if self.ticks_since_grow > 20:
            if self.food_count < 3:
                self.food_count += 1
            self.ticks_since_grow = 0

