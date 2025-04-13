import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def func(eq, t, r1, l1, l2, beta):
    x,y = eq
    return [r1*x-l1*x*y,l2*x*y-beta*y]

def solution(t0=0, t1=1000, num_points=1000, r1=0.5, l1=0.01, l2=0.01, beta=0.2, x0=25, y0=5):
    ti=np.arange(t0, t1, 1/num_points)
    n0=[x0,y0]
    sol=odeint(func,n0,ti,args=(r1, l1, l2, beta))

    x=sol[:,0]
    y=sol[:,1]

    plt.subplot(121)
    plt.plot(ti,x,"red",label="x",lw=1)
    plt.plot(ti, y, "green", label="y", lw=1)
    plt.xlabel("t", fontsize=17)
    plt.ylabel("x,y", fontsize=17)
    plt.grid()
    plt.legend()
    plt.title("a")

    plt.subplot(122)
    plt.plot(x,y, "red", label="x", lw=1)
    plt.xlabel("x", fontsize=17)
    plt.ylabel("y", fontsize=17)
    plt.grid()
    plt.title("b")
    plt.tight_layout()
    plt.savefig("Task4.png")
    plt.show()

if __name__ == "__main__":
    solution()