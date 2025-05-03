import simpy
import numpy as np

class SimulationModel:
    def __init__(self, arrival_rate, service_time, num_pumps, simulation_time=1000, sampling_interval=0.1):
        self.arrival_rate = arrival_rate
        self.service_time = service_time
        self.num_pumps = num_pumps
        self.simulation_time = simulation_time
        self.sampling_interval = sampling_interval

    def run_simulation(self, queue_limit=None):
        env = simpy.Environment()
        station = simpy.Resource(env, capacity=self.num_pumps)
        wait_times = []
        lost_cars = 0
        state_samples = []

        def monitor_state():
            while True:
                state_samples.append((env.now, len(station.queue), station.count))
                yield env.timeout(self.sampling_interval)
        env.process(monitor_state())

        def refuel_car(car_id):
            nonlocal lost_cars
            arrival_time = env.now
            if queue_limit is not None and len(station.queue) >= queue_limit:
                lost_cars += 1
                return
            with station.request() as req:
                yield req
                service_duration = np.random.exponential(self.service_time)
                yield env.timeout(service_duration)
                wait_times.append(env.now - arrival_time)

        def car_generator():
            car_id = 0
            while True:
                interarrival_time = np.random.exponential(1.0 / self.arrival_rate)
                yield env.timeout(interarrival_time)
                env.process(refuel_car(car_id))
                car_id += 1

        env.process(car_generator())
        env.run(until=self.simulation_time)

        queue_lengths = [q for _, q, _ in state_samples]
        busy_counts  = [b for _, _, b in state_samples]
        Lq = np.mean(queue_lengths)
        Ls = np.mean([q + b for q, b in zip(queue_lengths, busy_counts)])
        idle_samples = sum(1 for q, b in zip(queue_lengths, busy_counts) if (q + b) == 0)
        P0 = idle_samples / len(state_samples) if state_samples else 0.0
        Wq = np.mean(wait_times) if wait_times else 0.0

        result = {
            "P0 (вероятность простоя)": P0,
            "Lq (среднее число машин в очереди)": Lq,
            "Ls (среднее число машин в системе)": Ls,
            "Wq (среднее время ожидания в очереди)": Wq,
            "Число потерянных машин": lost_cars
        }
        return result