import matplotlib
from matplotlib import pyplot as plt

from stats import *

matplotlib.use('TkAgg')


def sort_tasks(tasks: list[list[Task]]) -> list[Task]:
    tasks_arrival_time_sorted = []
    number_of_tasks = sum(len(t) for t in tasks)
    indices = [0] * len(tasks)
    for _ in range(number_of_tasks):
        min_index, min_val = 0, np.inf
        for i in range(len(tasks)):
            if indices[i] >= len(tasks[i]):
                continue
            if tasks[i][indices[i]].arrival_time < min_val:
                min_index = i
                min_val = tasks[i][indices[i]].arrival_time
        # min_index = np.argmin([tasks_to_sort[i][indices[i]].arrival_time for i in range(number_of_vehicles)])

        tasks_arrival_time_sorted.append(tasks[min_index][indices[min_index]])
        indices[min_index] += 1
    return tasks_arrival_time_sorted


def print_tasks_generator_sorted(tasks: list[list[Task]]):
    for v in tasks:
        for t in v:
            print(t.generator, t.arrival_time, t.service_begin_time, t.service_time, t.service_end_time,
                  t.executor_processor, t.priority)


def print_tasks_generated_by(tasks: list[list[Task]], task_generator_name: str):
    for v in tasks:
        if v[0].generator != task_generator_name:
            continue
        for t in v:
            print(t.generator, t.arrival_time, t.service_begin_time, t.service_time, t.service_end_time,
                  t.executor_processor, t.priority)


def print_tasks_executed_by(tasks: list[list[Task]], task_executor_name: str):
    for v in tasks:
        for t in v:
            if t.executor_processor == task_executor_name:
                print(t.generator, t.arrival_time, t.service_begin_time, t.service_time, t.service_end_time,
                      t.executor_processor, t.priority)


def print_tasks_time_sorted(tasks: list[list[Task]]):
    for t in sort_tasks(tasks):
        print(t.generator, t.arrival_time, t.service_begin_time, t.service_time, t.service_end_time,
              t.executor_processor, t.priority)


def print_mean_length_of_queues(tasks: list[list[Task]], simulation_time: float, processor_names: list[str],
                                vehicle_processor_names: list[str], vehicle_processor_shut_down_times: list[float]):
    for processor in processor_names:
        print(f'Mean length of queue {processor}: {mean_length_of_queue(tasks, processor, simulation_time)}')
    for idx, vehicle in enumerate(vehicle_processor_names):
        print(f'Mean length of queue {vehicle}: '
              f'{mean_length_of_queue(tasks, vehicle, simulation_time - vehicle_processor_shut_down_times[idx])}')


def print_mean_time_spent_in_queues(tasks: list[list[Task]]) -> None:
    print(f'Average time spent in all queues: {mean_time_spent_in_queues(tasks)}')


def print_mean_time_spent_in_each_queue(tasks: list[list[Task]], queue_names: list[str]) -> None:
    for queue in queue_names:
        print(f'Average time spent by tasks in queue {queue}: {mean_time_spent_in_a_queue(tasks, queue)}')


def print_utilization_of_each_processor(tasks: list[list[Task]], simulation_time: float, processor_names: list[str],
                                        vehicle_processor_names: list[str],
                                        vehicle_processor_shut_down_times: list[float]):
    for processor in processor_names:
        print(f'Utilization of processor {processor}: {utilization_of_processor(tasks, processor, simulation_time)}')
    for idx, vehicle in enumerate(vehicle_processor_names):
        print(f'Utilization of processor {vehicle}: '
              f'{utilization_of_processor(tasks, vehicle, simulation_time - vehicle_processor_shut_down_times[idx])}')


def visualize_cdf_plot_of_times_spent_in_queues(tasks: list[list[Task]], simulation_time: float, queue_names: list[str],
                                                step: float = 0.2, canvas_time: int = -1) -> None:
    time_in_queue_cdfs = []
    for queue in queue_names:
        time_in_queue_cdfs.append(waiting_time_cdf(tasks, queue, simulation_time, step))

    number_of_rows = ceil(len(queue_names) / 2)
    number_of_columns = 2
    fig, ax = plt.subplots(number_of_rows, number_of_columns, figsize=(10, 3 * number_of_rows))

    for i in range(number_of_rows):
        for j in range(number_of_columns):
            index = number_of_columns * i + j
            x = [step * i for i in range(len(time_in_queue_cdfs[index][0]))]
            for k in range(len(time_in_queue_cdfs[index])):
                ax[i, j].plot(x, time_in_queue_cdfs[index][k], label=list(Priority)[k].name + ' Priority')
            ax[i, j].set_xlabel(f'Time Spent in Queue {queue_names[index]}')
            ax[i, j].set_ylabel('Probability')
            ax[i, j].grid()
            ax[i, j].legend()
            # ax[i, j].set_title(f'CDF Plot of Tasks\' Time Spent in Queue {queue_names[index]}')

    if canvas_time > 0:
        timer = fig.canvas.new_timer(interval=canvas_time)
        timer.add_callback(lambda: plt.close())
        timer.start()

    plt.show()
