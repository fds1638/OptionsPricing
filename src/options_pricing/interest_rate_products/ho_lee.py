import matplotlib.pyplot as plt
from typing import Callable, Generator
import numpy as np
import math

class HoLee():
    @classmethod
    def create(cls, theta, sigma):
        """Return HoLee instance depending on whether or not theta is defined by a function or an array."""
        if isinstance(theta, Callable):
            # theta is a function
            return HoLeeFunction(theta, sigma)
        elif isinstance(theta, list):
            # theta is a list
            return HoLeeList(theta, sigma)
        else:
            raise ValueError("Invalid argument type")

class HoLeeFunction(HoLee):
    """HoLee when theta is defined as a function."""
    def __init__(self, theta: Callable[float,float] = lambda x : 0, sigma: float = 0.01):
        self.theta = theta
        self.sigma = sigma # sigma is always a float

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

    def eval_ZCB_price(self, t:float, T:float, P0: Callable, f0: Callable, r: Callable) -> float:
        """Ho-Lee formula for P(t,T)."""
        A = math.exp(
            math.log(P0(T) / P0(t))
            + f0(t) * (T - t)
            - 0.5 * self.sigma * self.sigma * t * (T - t) * (T - t)
        )
        return A * math.exp(-r(t) * (T - t))


class HoLeeList(HoLee):
    """HoLee when theta is defined as a function."""
    def __init__(self, theta: list = [], sigma: float = 0.01):
        self.theta = theta
        self.sigma = sigma # sigma is always a float

    def eval_theta_list(self, r0: float, dt: float, theta_vec: list):
        rng = np.random.default_rng()
        retval = [r0]
        for ii in range(len(theta_vec)):
            r_prev = retval[-1]
            retval.append(
                r_prev + theta_vec[ii] * dt + self.sigma * rng.standard_normal() * math.pow(dt, 0.5)
            )
        return retval
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

