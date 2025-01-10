import numpy as np

from task import Task, Priority
from utils import sort_tasks


class QueueDiscipline:
    def __init__(self):
        self._tasks = None

    def get_next_task(self, time: float):
        if not self._tasks:
            return None
        return self._tasks.pop(0)

    def determine_tasks(self, tasks: list[list[Task]]) -> None:
        self._tasks = sort_tasks(tasks)

    def _length_queue(self, time: float) -> int:
        last_index = len(self._tasks) - 1
        for i in range(len(self._tasks)):
            if self._tasks[i].arrival_time > time:
                last_index = i - 1
                break
        return last_index + 1


class FIFOQueueDiscipline(QueueDiscipline):
    def get_next_task(self, time: float):
        if not self._tasks:
            return None
        return self._tasks.pop(0)


class NPPSQueueDiscipline(QueueDiscipline):
    def get_next_task(self, time: float):
        if not self._tasks:
            return None
        queue_length = self._length_queue(time)
        if queue_length == 0:
            return self._tasks.pop(0)
        else:
            chosen_index = np.argmin([self._tasks[i].priority.value for i in range(queue_length)])
            return self._tasks.pop(chosen_index)


class WRRQueueDiscipline(QueueDiscipline):
    def __init__(self):
        super().__init__()
        self.__task_priority_index = 0
        self.__number_of_occurrences_of_priority = 0

    def get_next_task(self, time: float):
        if not self._tasks:
            return None
        queue_length = self._length_queue(time)
        if queue_length == 0:
            task = self._tasks.pop(0)
            self.__task_priority_index = list(Priority).index(task.priority)
            self.__number_of_occurrences_of_priority = 1
        else:
            task = None
            priority_index = self.__task_priority_index
            while task is None:
                for i in range(queue_length):
                    if self._tasks[i].priority == list(Priority)[priority_index]:
                        task = self._tasks.pop(i)
                        break
                if task is None:
                    priority_index = (priority_index + 1) % len(Priority)
            if self.__task_priority_index == priority_index:
                self.__number_of_occurrences_of_priority += 1
            else:
                self.__task_priority_index = priority_index
                self.__number_of_occurrences_of_priority = 1

        priority_weight = len(Priority) + 1 - list(Priority)[self.__task_priority_index].value
        if self.__number_of_occurrences_of_priority >= priority_weight:
            self.__task_priority_index = (self.__task_priority_index + 1) % len(Priority)
            self.__number_of_occurrences_of_priority = 0
        return task
