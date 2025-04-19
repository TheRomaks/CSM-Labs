import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def f1(y, t):
    return y**2 - t*y

def f2(y, t):
    return y**2 + 1

def solution(t0,t1,num_points):
    t_values = np.arange(t0,t1,1/num_points)

    y0 = 0.0

    y_solution_1 = odeint(f1, y0, t_values)

    y_solution_2 = odeint(f2, y0, t_values)

    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.plot(t_values, y_solution_1, 'b', label="Численное решение")
    plt.title("y' = y^2 - t*y, y(0)=0")
    plt.xlabel("t")
    plt.ylabel("y(t)")
    plt.legend()
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(t_values, y_solution_2, 'b', label="Численное решение")
    plt.title("y' = y^2 + 1, y(0)=0")
    plt.xlabel("t")
    plt.ylabel("y(t)")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("Task1.png")
    plt.show()

if __name__ == "__main__":
    solution(0,1,100)