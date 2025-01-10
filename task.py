from enum import Enum
from types import DynamicClassAttribute


class Priority(Enum):
    LOW = 3
    MID = 2
    HIGH = 1

    @DynamicClassAttribute
    def name(self):
        name = super().name.lower().capitalize()
        return name


class Task:
    def __init__(self, priority: Priority, arrival_time: float, task_generator: str):
        self.priority = priority
        self.arrival_time = arrival_time
        self.generator = task_generator
        self.service_time = None
        self.service_begin_time = None
        self.service_end_time = None
        self.executor_processor = None
