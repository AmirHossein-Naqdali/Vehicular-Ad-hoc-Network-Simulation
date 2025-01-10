import numpy as np

from queue_discipline import WRRQueueDiscipline, FIFOQueueDiscipline, NPPSQueueDiscipline
from task import Task
from vehicle import Vehicle


class ControlUnit:
    def __init__(self, service_rate: float, transfer_time_overhead: float, transfer_probability: float,
                 vehicles: list[Vehicle], number_of_processors: int = 1, queue_discipline: str = 'FIFO'):
        self.__tasks_executed_by_each_processor = [[] for _ in range(number_of_processors)]
        self.__number_of_processors = number_of_processors
        self.__service_rate = service_rate
        self.__transfer_time_overhead = transfer_time_overhead
        self.__transfer_probability = transfer_probability
        self.__vehicles = vehicles
        self.__queue_discipline = {'FIFO': FIFOQueueDiscipline, 'NPPS': NPPSQueueDiscipline,
                                   'WRR': WRRQueueDiscipline}.get(queue_discipline.upper(), 'FIFO')()

    def execute_tasks(self, tasks: list[list[Task]]) -> None:
        self.__queue_discipline.determine_tasks(tasks)

        number_of_vehicles = len(self.__vehicles)
        number_of_tasks = sum(len(t) for t in tasks)
        service_time = np.random.exponential(1 / self.__service_rate, size=number_of_tasks)

        current_time = 0
        for i in range(number_of_tasks):
            task = self.__queue_discipline.get_next_task(current_time)
            parked_vehicles = [i for i in range(number_of_vehicles) if
                               self.__vehicles[i].parking_time <= task.arrival_time]
            transfer_task = parked_vehicles and (np.random.random() <= self.__transfer_probability)

            if not transfer_task:
                self.__execute_task_in_processor(task, service_time[i])
            else:
                vehicle_to_execute_the_task = np.random.choice(parked_vehicles)
                if task.generator[1:] != str(vehicle_to_execute_the_task):
                    self.__execute_task_in_vehicle(task, vehicle_to_execute_the_task)
                else:
                    self.__execute_task_in_processor(task, service_time[i])
            task.service_end_time = task.service_begin_time + task.service_time
            current_time = self.__get_current_time()

    def __execute_task_in_processor(self, task: Task, service_time: float):
        processor_number, service_begin_time = self.__task_begin_time(task)
        task.service_begin_time = service_begin_time
        task.service_time = service_time
        task.executor_processor = 'P' + str(processor_number)
        self.__tasks_executed_by_each_processor[processor_number].append(task)

    def __execute_task_in_vehicle(self, task: Task, vehicle_index: int):
        service_begin_time = self.__vehicles[vehicle_index].execute_task(task, task.arrival_time +
                                                                         self.__transfer_time_overhead)
        task.service_begin_time = service_begin_time
        task.executor_processor = 'V' + str(vehicle_index)

    def __get_current_time(self) -> float:
        for tasks_of_processor in self.__tasks_executed_by_each_processor:
            if not tasks_of_processor:
                return 0
        current_time = np.min([tasks_of_processor[-1].service_end_time
                               for tasks_of_processor in self.__tasks_executed_by_each_processor])
        return current_time

    def __task_begin_time(self, task: Task):
        for processor_index, tasks_of_processor in enumerate(self.__tasks_executed_by_each_processor):
            if not tasks_of_processor or tasks_of_processor[-1].service_end_time <= task.arrival_time:
                return processor_index, task.arrival_time
        index = np.argmin([self.__tasks_executed_by_each_processor[i][-1].service_end_time
                           for i in range(self.__number_of_processors)])
        return index, self.__tasks_executed_by_each_processor[index][-1].service_end_time
