import pandas as pd
from pathlib import Path

from world.data_enums import GlobalMetric
#from world.game_tick_manager import GameTickManager


# Todo: make a folder for the data collection classes
from world.game_tick_dto import GameTickDto


class DataCollector:

    def __init__(self, tick_dto: GameTickDto):
        self.tick_dto = tick_dto
        self.start_day = self.tick_dto.day
        self.data = {m.name: [] for m in GlobalMetric}

    def add_data(self, metric: GlobalMetric):
        metric_data = self.data.get(metric.name)
        while len(metric_data) - 1 < self.get_index():
            metric_data.append(0)
        metric_data[self.get_index()] += 1

    def save_data(self, generation):
        filepath = Path('data/global_data_day_x_to_y.csv')
        df = pd.DataFrame({})
        df.index += 1
        df.index.name = 'day'
        df.to_csv(filepath)

    def get_index(self):
        return self.tick_dto.day - self.start_day
