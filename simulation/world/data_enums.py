from enum import Enum


class GlobalMetric(Enum):
    DEATHS = 1,
    BIRTHS = 2,
    DEATHS_BY_STARVATION = 4,
    BERRIES_COLLECTED = 8,
    BERRIES_GROWN = 16,
    DAY = 32

