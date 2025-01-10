import numpy as np

from task import Task, Priority


class Vehicle:
    def __init__(self, task_production_rate: float, service_execution_rate: float, parking_time: float = np.inf):
        self.__tasks_to_execute = []
        self.__task_production_rate = task_production_rate
        self.__task_execution_rate = service_execution_rate
        self.parking_time = parking_time

    def generate_tasks(self, time_threshold: float, vehicle_number: int) -> list[Task]:
        tasks = [Task(Priority.HIGH, 0, 'V' + str(vehicle_number))]
        bunch_size = int(self.__task_production_rate * time_threshold / 2)
        priority_sum = sum(p.value for p in Priority)
        priority_scale = priority_sum * 4
        priority_offset = (priority_scale - priority_sum) / len(Priority)
        priority_probs = [(p.value + priority_offset) / priority_scale for p in Priority]
        while True:
            priorities = np.random.choice([p for p in Priority], p=priority_probs, size=bunch_size)
            inter_arrival_times = np.random.exponential(1 / self.__task_production_rate, size=bunch_size)
            for i in range(bunch_size):
                arrival_time = inter_arrival_times[i] + tasks[-1].arrival_time
                if arrival_time > min(time_threshold, self.parking_time):
                    return tasks[1:]
                task = Task(priorities[i], arrival_time, 'V' + str(vehicle_number))
                tasks.append(task)

    def execute_task(self, task: Task, arrival_time: float) -> float:
        task.service_time = np.random.exponential(1 / self.__task_execution_rate)
        service_begin = arrival_time
        if self.__tasks_to_execute:
            service_begin = max(self.__tasks_to_execute[-1].service_end_time, arrival_time)
        self.__tasks_to_execute.append(task)
        return service_begin
