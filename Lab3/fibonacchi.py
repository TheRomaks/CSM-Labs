import math
import numpy as np
from matplotlib import pyplot as plt

def f(x):
    return (x ** 2 - 2 * x + 2) * math.exp(-x)

def generate_fibonacci(n):
    fib = [1, 1]
    for i in range(2, n + 1):
        fib.append(fib[-1] + fib[-2])
    return fib

def fibonacci_search(a, b, epsilon, extr="min"):
    iteration_count = 0

    n = 1
    while True:
        fib = generate_fibonacci(n)
        if (b - a) / epsilon <= fib[-1]:
            break
        n += 1

    fib = generate_fibonacci(n)

    x1 = a + (b - a) * fib[n - 2] / fib[n]
    x2 = a + (b - a) * fib[n - 1] / fib[n]

    for i in range(n - 1):
        iteration_count += 1

        if extr == "min":
            if f(x1) < f(x2):
                b = x2
                x2 = x1
                x1 = a + (b - a) * fib[n - i - 3] / fib[n - i - 1]
            else:
                a = x1
                x1 = x2
                x2 = a + (b - a) * fib[n - i - 2] / fib[n - i - 1]
        elif extr == "max":
            if f(x1) > f(x2):
                b = x2
                x2 = x1
                x1 = a + (b - a) * fib[n - i - 3] / fib[n - i - 1]
            else:
                a = x1
                x1 = x2
                x2 = a + (b - a) * fib[n - i - 2] / fib[n - i - 1]
        else:
            raise ValueError("extr должен быть 'min' или 'max'")

    return (a + b) / 2, iteration_count

def fibonacci_search_both(a, b, epsilon):
    candidate_min, it_min = fibonacci_search(a, b, epsilon, extr="min")
    candidate_max, it_max = fibonacci_search(a, b, epsilon, extr="max")


    points = [
        (candidate_min, f(candidate_min)),
        (candidate_max, f(candidate_max)),
    ]
    global_min = min(points, key=lambda x: x[1])
    global_max = max(points, key=lambda x: x[1])

    return (global_min[0], global_min[1], it_min), (global_max[0], global_max[1], it_max)

if __name__ == "__main__":
    a = -600
    b = 20
    epsilon = 0.01

    global_min, global_max = fibonacci_search_both(a, b, epsilon)

    print(f"Глобальный минимум: x = {global_min[0]:.4f}, f(x) = {global_min[1]:.4f}, итераций = {global_min[2]}")
    print(f"Глобальный максимум: x = {global_max[0]:.4f}, f(x) = {global_max[1]:.4f}, итераций = {global_max[2]}")

    # График
    x_values = np.linspace(a, b, 1000)
    y_values = [f(x) for x in x_values]

    plt.figure(figsize=(12, 8))
    plt.plot(x_values, y_values, label='f(x)')

    plt.plot(global_min[0], global_min[1], 'go', markersize=10, label='Глобальный минимум')
    plt.plot(global_max[0], global_max[1], 'ro', markersize=10, label='Глобальный максимум')

    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('График функции f(x) с глобальными экстремумами')
    plt.grid(True)
    plt.legend()
    plt.show()
