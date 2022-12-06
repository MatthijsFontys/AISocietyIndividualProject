from enum import Enum


class GlobalMetric(Enum):
    DEATHS = 1,
    BIRTHS = 2,
    DEATHS_BY_STARVATION = 4,
    BERRIES_FORAGED = 8,
    BERRIES_GROWN = 16,
    TREES_IGNITED = 32,
    DEATHS_BY_HYPOTHERMIA = 64,

