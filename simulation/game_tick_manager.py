# manages everything in the world that doesn't need to be updated every frame
# for now should help with fruit regrowth and increasing survivor fitness


# the only thing that needs to be updated every frame and thus not managed by game ticks are the player's actions

class GameTickManager:

    def __init__(self, trees, survivors):
        self.trees = trees
        self.survivors = survivors
        self.tick_interval = 10
        self.tick_counter = 0

    def tick(self):

        self.tick_counter += 1
        if self.tick_counter >= self.tick_interval:
            for tree in self.trees:
                tree.try_grow_food()

            # reversed so that elements can be removed while looping through
            for survivor in reversed(self.survivors):
                survivor.increase_fitness()
                survivor.decrease_fullness()
                if survivor.is_dead():
                    self.survivors.remove(survivor)

            self.tick_counter = 0


        # check and create offspring

