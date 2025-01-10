from utils import *
from control_unit import ControlUnit
from vehicle import Vehicle

np.random.seed(2024)

# Vehicles
chi_task_production_mean = 3 / 7
lambda_two_vehicle_task_execution_rate = 1
number_of_vehicles = 3
vehicles = [Vehicle(1 / chi_task_production_mean, lambda_two_vehicle_task_execution_rate) for _ in
            range(number_of_vehicles)]
t_shut_down_time = 50
vehicles[0].parking_time = t_shut_down_time

# Tasks
T_simulation_time = 100
tasks = [v.generate_tasks(T_simulation_time, i) for i, v in enumerate(vehicles)]

# Control Unit
lambda_one_control_unit_task_execution_rate = 2
C_transfer_time_overhead = 0.3
P_probability_of_task_delegation = 0.25
N_number_of_processors = 3
queue_disciplines = ['FIFO', 'NPPS', 'WRR']
cu = ControlUnit(lambda_one_control_unit_task_execution_rate, C_transfer_time_overhead,
                 P_probability_of_task_delegation, vehicles, N_number_of_processors, queue_disciplines[0])

# Execution
cu.execute_tasks(tasks)

# Results
T_simulation_time = np.max(
    [tasks[i][j].service_end_time for i in range(number_of_vehicles) for j in range(len(tasks[i]))])
print(f'Simulation Time: {T_simulation_time}')

# print('----------------------------------------------------------------------------')
# print_tasks_generator_sorted(tasks)

# print('----------------------------------------------------------------------------')
# print_tasks_generated_by(tasks, 'V0')

# print('----------------------------------------------------------------------------')
# print_tasks_executed_by(tasks, 'V0')

# print('----------------------------------------------------------------------------')
# print_tasks_time_sorted(tasks)

processor_names = ['P' + str(i) for i in range(N_number_of_processors)]
vehicle_processor_names = ['V0']
vehicle_processor_shut_down_times = [t_shut_down_time]
queue_names = processor_names + vehicle_processor_names

print('----------------------------------------------------------------------------')
print_mean_length_of_queues(tasks, T_simulation_time, processor_names, vehicle_processor_names,
                            vehicle_processor_shut_down_times)

print('----------------------------------------------------------------------------')
print_mean_time_spent_in_queues(tasks)

print('----------------------------------------------------------------------------')
print_mean_time_spent_in_each_queue(tasks, queue_names)

print('----------------------------------------------------------------------------')
print_utilization_of_each_processor(tasks, T_simulation_time, processor_names, vehicle_processor_names,
                                    vehicle_processor_shut_down_times)

print('----------------------------------------------------------------------------')
visualize_cdf_plot_of_times_spent_in_queues(tasks, T_simulation_time, queue_names, step=0.05, canvas_time=5000)
# visualize_cdf_plot_of_times_spent_in_queues(tasks, T_simulation_time, queue_names, step=0.05)
