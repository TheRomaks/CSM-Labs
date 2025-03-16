# compare_iterations.py
import numpy as np

from fibonacchi import fibonacci_search_both
from newton_math import compute_extrema

def compare_iterations():
    eps_list = [1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7]

    print("Сравнение числа итераций для разных значений eps:")
    print("-------------------------------------------------\n")

    a,b=-600,200
    initial_guess = 0
    max_iter = 100

    print("Метод Фибоначчи (поиск минимума и максимума):")
    print("eps      | Итерации (min) | Итерации (max)")
    print("-----------------------------------------")

    for eps in eps_list:
        (xmin, fmin, it_min), (xmax, fmax, it_max) = fibonacci_search_both(a, b, eps)
        print(f"{eps:1.0e}   | {it_min:^15d} | {it_max:^15d}")

    print("\nМетод Ньютона (поиск одной критической точки):")
    print("eps      | Итерации Ньютона")
    print("---------------------------")

    for eps in eps_list:
        data = compute_extrema(a, b, initial_guess, eps, max_iter)
        newt_iter = data['iteration_count']
        print(f"{eps:1.0e}   | {newt_iter:^18d}")

if __name__ == "__main__":
    compare_iterations()
