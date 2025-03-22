import matplotlib.pyplot as plt
import numpy as np
import math

def brownian_motion_0_to_1(dt = 0.01, mu = 0, dX_dt_exp = 0.5):
    """Brownian motion on an interval from t=0 to t=1."""
    t = [i * dt for i in range(int(1/dt)+1)]
    y = [None for i in range(int(1/dt)+1)]
    y[0] = 0

    rng = np.random.default_rng()

    for timestep in range(1, int(1/dt)+1):
        y[timestep] = y[timestep-1] + mu * dt + rng.standard_normal() * math.pow(dt, dX_dt_exp)

    return t, y

if __name__=="__main__":
    """Show that relation between dX and dt must be dX ~ sqrt(dt)."""

    # Choose dt values that will show which scaling will work.
    dt_values = [0.001, 0.00001, 0.0000001]

    # dX = dt^0.25 so as dt -> 0 the Brownian motion will go to infinity.
    for dt in dt_values:
        t, y = brownian_motion_0_to_1(dt, 0, 0.25)
        plt.plot(t.copy(), y.copy())
    plt.legend([f'dt {dt}' for dt in dt_values], loc="upper left")
    plt.show()

    # dX = dt^0.75 so as dt -> 0 the Brownian motion will go to zero.
    for dt in dt_values:
        t, y = brownian_motion_0_to_1(dt, 0, 0.75)
        plt.plot(t.copy(), y.copy())
    plt.legend([f'dt {dt}' for dt in dt_values], loc="upper left")
    plt.show()

    # dX = dt^0.50 so as dt -> 0 the Brownian motion will be scaled properly.
    for dt in dt_values:
        t, y = brownian_motion_0_to_1(dt, 0, 0.50)
        plt.plot(t.copy(), y.copy())
    plt.legend([f'dt {dt}' for dt in dt_values], loc="upper left")
    plt.show()
