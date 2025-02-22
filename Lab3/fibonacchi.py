import math

def f(x):
    return (x ** 2 - 2 * x + 2) * math.exp(-x)

def generate_fibonacci(n):
    fib = [1, 1]
    for i in range(2, n + 1):
        fib.append(fib[-1] + fib[-2])
    return fib


def fibonacci_search(a, b, epsilon, mode="min"):
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
        if mode == "min":
            if f(x1) < f(x2):
                b = x2
                x2 = x1
                x1 = a + (b - a) * fib[n - i - 3] / fib[n - i - 1]
            else:
                a = x1
                x1 = x2
                x2 = a + (b - a) * fib[n - i - 2] / fib[n - i - 1]
        elif mode == "max":
            if f(x1) > f(x2):
                b = x2
                x2 = x1
                x1 = a + (b - a) * fib[n - i - 3] / fib[n - i - 1]
            else:
                a = x1
                x1 = x2
                x2 = a + (b - a) * fib[n - i - 2] / fib[n - i - 1]
        else:
            raise ValueError("mode должен быть 'min' или 'max'")

    return (a + b) / 2


def fibonacci_search_both(a, b, epsilon):

    candidate_min = fibonacci_search(a, b, epsilon, mode="min")
    candidate_max = fibonacci_search(a, b, epsilon, mode="max")

    # points = [
    #     (a, f(a)),
    #     (candidate_min, f(candidate_min)),
    #     (candidate_max, f(candidate_max)),
    #     (b, f(b))
    # ]

    points = [
        (candidate_min, f(candidate_min)),
        (candidate_max, f(candidate_max)),
    ]

    global_min = min(points, key=lambda x: x[1])
    global_max = max(points, key=lambda x: x[1])
    return global_min, global_max



a = -500
b = 20
epsilon = 0.01

global_min, global_max = fibonacci_search_both(a, b, epsilon)

print(f"Глобальный минимум: x = {global_min[0]:.4f}, f(x) = {global_min[1]:.4f}")
print(f"Глобальный максимум: x = {global_max[0]:.4f}, f(x) = {global_max[1]:.4f}")
