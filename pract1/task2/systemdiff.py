from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

def func(eq,t,a,b,c):
    y1,y2,y3=eq
    return [-y2-y3,y1+a*y2,b+y3*(y1-c)]

def solution(a,b,c,t0,t1,num_points):
    ti=np.arange(t0,t1,1/num_points)
    y0=[1,1,1]
    solution=odeint(func,y0,ti,args=(a, b, c))
    x = solution[:, 0]
    y = solution[:, 1]
    z = solution[:, 2]

    plt.figure(figsize=(10, 8))


    plt.subplot(221)
    plt.plot(x, y, lw=1)
    plt.title("Фазовый портрет")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid()


    plt.subplot(222)
    plt.plot(ti, x, lw=1, color="orange")
    plt.title("x(t)")
    plt.xlabel("t")
    plt.ylabel("x")
    plt.grid()


    plt.subplot(223)
    plt.plot(ti, y, lw=1, color="green")
    plt.title("y(t)")
    plt.xlabel("t")
    plt.ylabel("y")
    plt.grid()


    plt.subplot(224)
    plt.plot(ti, z, lw=1, color="red")
    plt.title("z(t)")
    plt.xlabel("t")
    plt.ylabel("z")
    plt.grid()

    plt.tight_layout()
    plt.savefig("Task2.png")
    plt.show()


if __name__ == "__main__":
    solution(0.2,0.2,5,0,100,100)