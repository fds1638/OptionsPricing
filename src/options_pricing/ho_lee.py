import matplotlib.pyplot as plt
from typing import Callable, Generator
import numpy as np
import math

class HoLee():
    def __init__(self, theta: Callable[float,float] = lambda x : 0, sigma: float = 0.01):
        self.theta = theta
        self.sigma = sigma

    def eval_float_arg(self, r0 : float, rng : Generator, dt: float):
        cur_theta = self.theta
        cur_theta_val = cur_theta(0)(r0)
        return r0 + cur_theta_val * dt + self.sigma * rng.standard_normal() * math.pow(dt, 0.5)

    def eval_time_T_step_dt(self, T: float, dt: float, r_begin: float):
        num_timesteps = int(T/dt)
        rng = np.random.default_rng()
        return_value = [r_begin for _ in range(num_timesteps + 1)]
        for i in range(1, num_timesteps + 1):
            return_value[i] = self.eval_float_arg(return_value[i-1], rng, dt)
        return return_value

if __name__=="__main__":
    time_values = [i/10 for i in range(0,101)]
    hl = HoLee(lambda x : lambda x: 0.005)
    interest_rates = hl.eval_time_T_step_dt(10, 0.1, 0.0)
    plt.plot(time_values, interest_rates,'o-')
    plt.legend([f"theta: {hl.theta}\n sigma: {hl.sigma}"])
    plt.show()

