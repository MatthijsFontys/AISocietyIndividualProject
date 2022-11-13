class TickCounter:

    def __init__(self, interval: int, is_on=True):
        self.interval = interval
        self.times_fired = 0
        self.counter = 0
        self.is_on = is_on
        self.has_fired = False

    def tick(self) -> bool:
        if not self.is_on:
            return False
        self.counter += 1
        did_fire = False
        if self.counter >= self.interval:
            self.times_fired += 1
            self.counter = 0
            self.has_fired = True
            did_fire = True
        return did_fire

    def get_has_fired(self):
        to_return = self.has_fired
        self.has_fired = False
        return to_return

    def reset(self):
        self.counter = 0

    def get_percentage(self):
        return self.counter / self.interval
