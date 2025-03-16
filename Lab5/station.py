import math

class AnalyticalModel:
    def __init__(self, arrival_rate, service_time, num_pumps):
        self.lambda_ = arrival_rate
        self.service_time = service_time
        self.num_pumps = num_pumps
        self.mu = 1.0 / service_time

    def mmn_no_limit_queue(self):
        n = self.num_pumps
        lambda_ = self.lambda_
        mu = self.mu
        rho = lambda_ / (n * mu)

        sum_term = sum((n * rho) ** k / math.factorial(k) for k in range(n))
        p0 = 1.0 / (sum_term + ((n * rho) ** n / (math.factorial(n) * (1 - rho))))

        Lq = ((n * rho) ** n * p0) / (math.factorial(n) * (1 - rho) ** 2)
        Ls = Lq + lambda_ / mu
        Wq = Lq / lambda_

        return {
            "P0 (вероятность простоя)": p0,
            "Lq (среднее число машин в очереди)": Lq,
            "Ls (среднее число машин в системе)": Ls,
            "Wq (среднее время ожидания в очереди, мин)": Wq
        }

    def mmn_limited_queue(self, max_queue):
        n = self.num_pumps
        lambda_ = self.lambda_
        mu = self.mu
        rho = lambda_ / (n * mu)
        K = n + max_queue

        sum_term = sum((n * rho) ** k / math.factorial(k) for k in range(n))
        sum_term += sum((n * rho) ** k / (math.factorial(n) * n ** (k - n)) for k in range(n, K + 1))
        p0 = 1.0 / sum_term
        Lq = sum((k - n) * ((n * rho) ** k / (math.factorial(n) * n ** (k - n))) * p0 for k in range(n, K + 1))
        P_block = ((n * rho) ** K / (math.factorial(n) * n ** (K - n))) * p0
        lambda_eff = lambda_ * (1 - P_block)
        Ls = Lq + lambda_eff / mu
        Wq = Lq / lambda_

        return {
            "P0 (вероятность простоя)": p0,
            "Lq (среднее число машин в очереди)": Lq,
            "Ls (среднее число машин в системе)": Ls,
            "Wq (среднее время ожидания в очереди, мин)": Wq,
            "P_block (вероятность отказа)": P_block
        }

def main():
    lambda_arrival = 1
    service_time = 3
    num_pumps = 4
    max_queue = 4

    print("Аналитическая модель (без ограничения очереди):")
    analytical_model = AnalyticalModel(lambda_arrival, service_time, num_pumps)
    results_no_limit = analytical_model.mmn_no_limit_queue()
    for key, value in results_no_limit.items():
        print(f"{key}: {value:.4f}")

    print("\nАналитическая модель (с ограниченной очередью):")
    results_limited = analytical_model.mmn_limited_queue(max_queue)
    for key, value in results_limited.items():
        print(f"{key}: {value:.4f}")

if __name__ == '__main__':
    main()

