from math import ceil

import numpy as np

from task import Task, Priority


def time_spent_in_a_queue(tasks: list[list[Task]], queue_name: str) -> float:
    time_spent_in_queue = sum((task.service_begin_time - task.arrival_time) for v in tasks for task in v
                              if task.executor_processor == queue_name)
    return time_spent_in_queue


def time_spent_in_all_queues(tasks: list[list[Task]]) -> float:
    time_spent_in_queues = sum((task.service_begin_time - task.arrival_time) for v in tasks for task in v)
    return time_spent_in_queues


def mean_length_of_queue(tasks: list[list[Task]], queue_name: str, simulation_time: float) -> float:
    return time_spent_in_a_queue(tasks, queue_name) / simulation_time


def number_of_tasks_in_a_queue(tasks: list[list[Task]], queue_name: str) -> int:
    number_tasks_in_queue = sum((task.executor_processor == queue_name) for v in tasks for task in v)
    return number_tasks_in_queue


def number_of_tasks(tasks: list[list[Task]]) -> int:
    number_tasks = sum(len(v) for v in tasks)
    return number_tasks


def mean_time_spent_in_a_queue(tasks: list[list[Task]], queue_name: str) -> float:
    return time_spent_in_a_queue(tasks, queue_name) / number_of_tasks_in_a_queue(tasks, queue_name)


def mean_time_spent_in_queues(tasks: list[list[Task]]) -> float:
    return time_spent_in_all_queues(tasks) / number_of_tasks(tasks)


def time_getting_service_in_a_queue(tasks: list[list[Task]], queue_name: str) -> float:
    time_getting_service_in_queue = sum(task.service_time for v in tasks for task in v
                                        if task.executor_processor == queue_name)
    return time_getting_service_in_queue


def utilization_of_processor(tasks: list[list[Task]], processor_name: str, simulation_time: float) -> float:
    return time_getting_service_in_a_queue(tasks, processor_name) / simulation_time


def waiting_time_cdf(tasks: list[list[Task]], queue_name: str, simulation_time: float,
                     step: float = 0.2) -> list[list[float]]:
    n = ceil(simulation_time / step)

    probs = [[0] * n for _ in range(len(Priority))]
    for priority_index, priority in enumerate(Priority):
        for v in tasks:
            for t in v:
                if t.executor_processor == queue_name and t.priority == priority:
                    first_occurrence = ceil((t.service_begin_time - t.arrival_time) / step)
                    if first_occurrence <= 0:
                        first_occurrence = 1
                    probs[priority_index][first_occurrence - 1] += 1

    cum_probs = [[0] * n for _ in range(len(Priority))]
    for idx, c in enumerate(cum_probs):
        c[0] = probs[idx][0]
        for i in range(1, n):
            c[i] = c[i - 1] + probs[idx][i]

    # remove sequence of ones at the end of probs
    max_index = np.max([np.min([i for i in range(len(c)) if c[i] == c[-1]]) for c in cum_probs]) + 1
    for i, c in enumerate(cum_probs):
        cum_probs[i] = [0.0] + [c[j] / c[-1] for j in range(max_index)]

    return cum_probs
