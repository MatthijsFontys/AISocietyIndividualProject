class TickCounter:

    def __init__(self, interval: int):
        self.interval = interval
        self.times_fired = 0
        self.counter = 0

    def tick(self) -> bool:
        self.counter += 1
        did_fire = False
        if self.counter >= self.interval:
            self.times_fired += 1
            self.counter = 0
            did_fire = True
        return did_fire

    def reset(self):
        self.counter = 0

    def get_percentage(self):
        return self.counter / self.interval
