import base64
import io
import numpy as np
import csv
from matplotlib import pyplot as plt
from scipy.integrate import odeint


def model(y,t, m, g, rho_liquid, r, mu):
    v, h = y
    V = (4 / 3) * np.pi * r ** 3
    k1 = 6 * np.pi * mu * r # Формула Стокса
    F_gravity = m * g
    F_archimedes = rho_liquid * V * g
    F_resistance = k1 * v
    a = (F_gravity - F_archimedes - np.sign(v) * F_resistance) / m
    dhdt = -v
    dvdt = a
    return [dvdt, dhdt]

def drop_ball_in_liquid(r, g, ball_density, liquid_density, mu, h):
    V = (4 / 3) * np.pi * r ** 3
    m = ball_density * V
    T = 10
    dt = 0.01
    N = int(T / dt)
    time = np.linspace(0, T, N)
    y0 = [0, h]
    solution = odeint(model, y0, time, args=(m, g, liquid_density, r, mu))
    v = solution[:, 0]
    h_arr = solution[:, 1]

    if np.any(h_arr <= 0):
        stop_idx = np.where(h_arr <= 0)[0][0]
        time = time[:stop_idx]
        v = v[:stop_idx]
        h_arr = h_arr[:stop_idx]

    with open('results.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Time (s)', 'Velocity (m/s)', 'Height (m)'])
        for t, velocity, height in zip(time, v, h_arr):
            csv_writer.writerow([t, velocity, height])

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(time, v, label='Скорость')
    plt.xlabel('Время t, с')
    plt.ylabel('Скорость v, м/с')
    plt.legend()
    plt.subplot(1, 2, 2)
    plt.plot(time, h_arr, label='Высота', color='r')
    plt.xlabel('Время t, с')
    plt.ylabel('Высота h, м')
    plt.legend()
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return img_b64

