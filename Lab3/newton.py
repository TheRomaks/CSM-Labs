import math

def f(x):
    return (x ** 2 - 2 * x + 2) * math.exp(-x)

def f_prime(x):
    return -math.exp(-x) * (x - 2) ** 2

def f_double_prime(x):
    return math.exp(-x) * (x ** 2 - 6 * x + 8)

def newton_method(x0, eps, max_iter):
    x = x0
    for i in range(max_iter):
        fp = f_prime(x)
        fdp = f_double_prime(x)
        if abs(fdp) < 1e-10:
            print("Вторая производная близка к нулю, остановка метода Ньютона.")
            break
        x_new = x - fp / fdp
        if abs(x_new - x) < eps:
            return x_new
        x = x_new
    return x


def classify_critical_point(x):
    second = f_double_prime(x)
    if second > 0:
        return "минимум"
    elif second < 0:
        return "максимум"
    else:
        return "неопределён"


def find_global_extrema(a, b, critical_point):
    points = [(a, f(a)), (b, f(b))]
    if a <= critical_point <= b:
        points.append((critical_point, f(critical_point)))
    global_min = min(points, key=lambda point: point[1])
    global_max = max(points, key=lambda point: point[1])
    return global_min, global_max


def compute_extrema(a, b, initial_guess, eps, max_iter):
    cp = newton_method(initial_guess, eps, max_iter)
    cp_type = classify_critical_point(cp)
    global_min, global_max = find_global_extrema(a, b, cp)
    return {
        "critical_point": cp,
        "critical_type": cp_type,
        "global_min": global_min,
        "global_max": global_max
    }

a = -500
b = 20
initial_guess = 0
eps = 1e-5
max_iter = 100

extrema_data = compute_extrema(a, b, initial_guess, eps, max_iter)

print(f"Найденная критическая точка: x = {extrema_data['critical_point']:.6f}")
print(f"Значение в критической точке = {f(extrema_data['critical_point']):.6f}")
print(f"Критическая точка является локальным {extrema_data['critical_type']}.")

print("\nГлобальные экстремумы на отрезке:")
print(f"Глобальный минимум: x = {extrema_data['global_min'][0]:.6f}, f(x) = {extrema_data['global_min'][1]:.6f}")
print(f"Глобальный максимум: x = {extrema_data['global_max'][0]:.6f}, f(x) = {extrema_data['global_max'][1]:.6f}")
