import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def system_y(y, t):
    x1, x2 = y
    dx1dt = x2
    dx2dt = np.cos(t) - 2*x2 - 3*x1
    return [dx1dt, dx2dt]

def system_z(Z, t,a):
    x1, x2 = Z
    dx1dt = x2
    dx2dt = a*(1 - x1**2)*x2 - x1
    return [dx1dt, dx2dt]

def solution(t_y0=0,t_y1=2*np.pi,t_z0=0,t_z1=30,num_points_y=1000,num_points_z=1000,a=1):
    t_y = np.linspace(t_y0, t_y1, num_points_y)
    t_z = np.linspace(t_z0, t_z1, num_points_z)

    Y0 = [0.0, 0.0]
    Z0 = [0.0, 0.0]

    sol_y = odeint(system_y, Y0, t_y)
    sol_z = odeint(system_z, Z0, t_z,args=(a,))

    plt.figure(figsize=(10,4))

    plt.subplot(1,2,1)
    plt.plot(t_y, sol_y[:, 0], label="y(t)", color="blue")
    plt.plot(t_y, sol_y[:, 1], label="y'(t)", color="red")
    plt.title("y'' + 2y' + 3y = cos(t)")
    plt.xlabel("t")
    plt.ylabel("Решение и его производная")
    plt.grid(True)
    plt.legend()

    plt.subplot(1,2,2)
    plt.plot(t_z, sol_z[:, 0], label="z(t)", color="blue")
    plt.plot(t_z, sol_z[:, 1], label="z'(t)", color="red")
    plt.title("z'' - (1-z^2)z' + z = 0")
    plt.xlabel("t")
    plt.ylabel("Решение и его производная")
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.savefig("Task3.png")
    plt.show()

if __name__ == "__main__":
    solution()