import math
from scipy.optimize import newton
import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return (x ** 2 - 2 * x + 2) * math.exp(-x)

def f_prime(x):
    return -math.exp(-x) * (x - 2) ** 2

def f_double_prime(x):
    return math.exp(-x) * (x ** 2 - 6 * x + 8)

def newton_method(start, end, step=1.0):
    critical_points = []
    x = start
    while x <= end:
        try:
            cp = newton(f_prime, x, tol=1e-6, maxiter=100)

            if not math.isinf(f_prime(cp)) and not math.isnan(f_prime(cp)):

                if not any(abs(cp - existing_cp) < 1e-4 for existing_cp in critical_points):
                    critical_points.append(cp)
        except RuntimeError:
            pass
        x += step
    return critical_points


def classify_critical_point(x):
    second = f_double_prime(x)
    if second > 0:
        return "минимум"
    elif second < 0:
        return "максимум"
    else:
        return "неопределён"


start_range = -2
end_range = 20

critical_points = newton_method(start_range, end_range)
critical_points.sort()

for cp in critical_points:
    classification = classify_critical_point(cp)
    print(f"  x = {cp:.4f}: {classification}")

x_values = np.linspace(start_range, end_range, 1000)
x_values_filtered = [x for x in x_values if abs(1 + np.sin(x)) > 1e-3]
y_values = [f(x) for x in x_values_filtered]


plt.figure(figsize=(10, 6))
plt.plot(x_values_filtered, y_values, label='f(x)')

for cp in critical_points:
    classification = classify_critical_point(cp)
    if classification == "минимум":
        plt.plot(cp, f(cp), 'go', label='Локальный минимум' if 'Локальный минимум' not in plt.gca().get_legend_handles_labels()[1] else "")
    elif classification == "максимум":
        plt.plot(cp, f(cp), 'ro', label='Локальный максимум' if 'Локальный максимум' not in plt.gca().get_legend_handles_labels()[1] else "")
    else:
        plt.plot(cp, f(cp), 'yo', label='Неопределённая точка' if 'Неопределённая точка' not in plt.gca().get_legend_handles_labels()[1] else "")

plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend()

plt.ylim(-10, 25)
plt.xlim(-25, 50)

plt.show()



