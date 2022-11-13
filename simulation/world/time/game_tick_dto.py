from world.time.tick_counter import TickCounter


class GameTickDto:

    def __init__(self, day, timer: TickCounter):
        self.day = day
        self.timer = timer

    def tick(self, new_day):
        if new_day:
            self.day += 1

    def get_day_percent(self):
        return self.timer.get_percentage()

    def get_days_precise(self):
        return self.day + self.get_day_percent()

