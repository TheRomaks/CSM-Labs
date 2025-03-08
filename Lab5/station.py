import math

def mmn_no_limit_queue(lambda_, mu, n):
    rho = lambda_ / (n * mu)

    sum_term = sum((n * rho) ** k / math.factorial(k) for k in range(n))
    p0 = 1 / (sum_term + ((n * rho) ** n / (math.factorial(n) * (1 - rho))))

    ls = lambda_ / mu

    lq = ((n * rho) ** n * p0) / (math.factorial(n) * (1 - rho) ** 2)

    wq = lq / lambda_

    return {
        "P0 (вероятность простоя)": p0,
        "Lq (среднее число машин в очереди)": lq,
        "Ls (среднее число машин в системе)": ls,
        "Wq (среднее время ожидания в очереди)": wq,
    }


def mmn_limited_queue(lambda_, mu, n, max_queue):
    rho = lambda_ / (n * mu)

    sum_term = sum((n * rho) ** k / math.factorial(k) for k in range(n))
    sum_term += sum((n * rho) ** k / (math.factorial(n) * n ** (k - n)) for k in range(n, n + max_queue + 1))
    p0 = 1 / sum_term

    lq = sum((k - n) * ((n * rho) ** k / (math.factorial(n) * n ** (k - n))) * p0 for k in range(n, n + max_queue + 1))
    wq = lq / lambda_

    return {
        "P0 (вероятность простоя)": p0,
        "Lq (среднее число машин в очереди)": lq,
        "Wq (среднее время ожидания в очереди)": wq,
    }


lambda_ = 1  # машина в минуту
mu = 1 / 3   # интенсивность обслуживания
n = 4        # количество колонок
max_queue = 4  # ограничение по очереди

print("Система без ограничения очереди:")
results_no_limit = mmn_no_limit_queue(lambda_, mu, n)
for key, value in results_no_limit.items():
    print(f"{key}: {value:.4f}")

print("\nСистема с ограниченной очередью:")
results_limited = mmn_limited_queue(lambda_, mu, n, max_queue)
for key, value in results_limited.items():
    print(f"{key}: {value:.4f}")
