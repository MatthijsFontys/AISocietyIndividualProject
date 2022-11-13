"""
Data collector mock, so data collected withing the waiting room isn't collected
"""
from world.data.data_enums import GlobalMetric


class MockCollector:

    def add_data(self, metric: GlobalMetric):
        pass

    def save_data(self, generation: int):
        pass

    def get_index(self) -> int:
        return -1

    def add_missing_values(self, metric, exclude_last):
        pass

