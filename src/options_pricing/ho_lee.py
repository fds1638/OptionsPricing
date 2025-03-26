import matplotlib.pyplot as plt
from typing import Callable, Generator
import numpy as np
import math

class HoLee():
    def __init__(self, theta: Callable[float,float] = lambda x : 0, sigma: float = 0.01):
        self.theta = theta
        self.sigma = sigma

    def eval_float_arg(self, r0 : float, rng : Generator, dt: float):
        return r0 + self.theta(r0) * dt + self.sigma * rng.standard_normal() * math.sqrt(dt)

    def eval_time_T_step_dt(self, T: float, dt: float):
        num_timesteps = int(T/dt)
        rng = np.random.default_rng()
        return_value = [0 for _ in range(num_timesteps + 1)]
        for i in range(1, num_timesteps + 1):
            return_value[i] = self.eval_float_arg(return_value[i-1], rng, dt)
        return return_value

if __name__=="__main__":
    time_values = [i/10 for i in range(0,101)]
    hl = HoLee(lambda x : 0.005)
    interest_rates = hl.eval_time_T_step_dt(10, 0.1)
    plt.plot(time_values, interest_rates,'o-')
    plt.legend([f"theta: {hl.theta}\n sigma: {hl.sigma}"])
    plt.show()

