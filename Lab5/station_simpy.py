import simpy
import numpy as np


def gas_station_simulation(env, num_pumps, arrival_rate, service_time, queue_limit=None):
    station = simpy.Resource(env, capacity=num_pumps)
    queue_lost = 0

    def refuel_car(env, car_id):
        nonlocal queue_lost
        arrival_time = env.now
        if queue_limit is not None and len(station.queue) >= queue_limit:
            queue_lost += 1
            return

        with station.request() as req:
            yield req
            yield env.timeout(np.random.poisson(service_time))
            wait_time = env.now - arrival_time
            wait_times.append(wait_time)

    def car_generator(env, arrival_rate):
        car_id = 0
        while True:
            yield env.timeout(np.random.poisson(1 / arrival_rate))
            env.process(refuel_car(env, car_id))
            car_id += 1

    wait_times = []
    env.process(car_generator(env, arrival_rate))
    env.run(until=1000)

    avg_wait = np.mean(wait_times) if wait_times else 0
    print(f"Среднее время ожидания: {avg_wait:.2f} мин.")
    if queue_limit is not None:
        print(f"Число потерянных машин: {queue_lost}")


# Тестовые параметры
lambda_arrival = 1  # машина в минуту
service_time = 3  # среднее время заправки
num_pumps = 4

print("=== Без ограничения очереди ===")
env = simpy.Environment()
gas_station_simulation(env, num_pumps, lambda_arrival, service_time)

print("\n=== Очередь ограничена 4 местами ===")
env = simpy.Environment()
gas_station_simulation(env, num_pumps, lambda_arrival, service_time, queue_limit=4)
