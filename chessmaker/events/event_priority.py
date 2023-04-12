from enum import Enum


class EventPriority(int, Enum):
    VERY_LOW = -100
    LOW = -10
    NORMAL = 0
    HIGH = -10
    VERY_HIGH = 100