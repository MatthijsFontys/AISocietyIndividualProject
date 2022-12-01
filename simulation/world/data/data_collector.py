import pandas as pd
from pathlib import Path

from world.data.data_enums import GlobalMetric

from world.time.game_tick_dto import GameTickDto
from world.time.tick_counter import TickCounter


class DataCollector:

    def __init__(self, tick_dto: GameTickDto, population_size: int):
        self.init_population_size = population_size
        self.tick_dto = tick_dto
        self.start_day = self.tick_dto.day
        self.data = {m.name: [] for m in GlobalMetric}
        self.day_counter = TickCounter(10)

    def add_data(self, metric: GlobalMetric):
        self.add_missing_values(metric, exclude_last=False)
        self.data.get(metric.name)[self.get_index()] += 1

    def save_data(self):
        for metric in GlobalMetric:
            self.add_missing_values(metric, exclude_last=True)
       #filepath = Path(f'world/data/csv/global_data_day_{self.start_day}_to_{self.get_index()}.csv')
        # Todo: change back to old filepath when not using path anymore for mount in azure container
        filepath = Path(f'checkpoints/global_data_day_{self.start_day}_to_{self.get_index()}.csv')
        self.data.update({'DAY': [i + 1 for i in range(self.get_index())]})

        df = pd.DataFrame(self.data)

        # COLUMNS derived from gathered data get prefixed with DER to show it can be derived from existing columns
        # Set additional columns derived from collected data
        df['DER_POP_DELTA'] = df[GlobalMetric.BIRTHS.name] - df[GlobalMetric.DEATHS.name]
        df['DER_POPULATION'] = df['DER_POP_DELTA'].cumsum() + self.init_population_size

        df.set_index('DAY', inplace=True)
        df.to_csv(filepath)

    def get_index(self) -> int:
        return self.tick_dto.day - self.start_day

    def tick(self, new_day: bool):
        if new_day:
            if self.day_counter.tick():
                self.save_data()

    def add_missing_values(self, metric, exclude_last):
        offset = 0 if exclude_last else 1
        metric_data = self.data.get(metric.name)
        while len(metric_data) - offset < self.get_index():
            metric_data.append(0)
