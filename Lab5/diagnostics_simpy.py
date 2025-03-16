import simpy
import random

class DiagnosticPost:
    def __init__(self, env, lambda_rate, service_time):
        self.env = env
        self.lambda_rate = lambda_rate
        self.service_time = service_time
        self.diagnostic = simpy.Resource(env, capacity=1)
        self.total_cars = 0
        self.served_cars = 0

    def diagnose(self):
        with self.diagnostic.request() as request:
            yield request
            yield self.env.timeout(random.expovariate(1 / self.service_time))
            self.served_cars += 1


def car_generator(env, post):
    while True:
        yield env.timeout(random.expovariate(post.lambda_rate))
        post.total_cars += 1
        env.process(post.diagnose())


def run_simulation(lambda_rate, service_time, sim_time):
    try:
        env = simpy.Environment()
        post = DiagnosticPost(env, lambda_rate, service_time)
        env.process(car_generator(env, post))
        env.run(until=sim_time)
        if post.total_cars > 0:
            p_otkaza = 1 - (post.served_cars / post.total_cars)
        else:
            p_otkaza = None
        q = 1 - p_otkaza if p_otkaza is not None else None
        A = lambda_rate * q if q is not None else None

        p0 = 1 - (post.diagnostic.count / sim_time)
        return {
            "p0": p0,
            "p_otkaza": p_otkaza,
            "q": q,
            "A": A,
            "total_cars": post.total_cars,
            "served_cars": post.served_cars
        }
    except Exception as e:
        raise RuntimeError("Ошибка при запуске симуляции: " + str(e))
