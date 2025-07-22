import matplotlib.pyplot as plt
from typing import Callable, Generator
import numpy as np
import math

class HullWhiteFunction():
    """Hull-White model."""

    def __init__(self, theta: Callable[float, float] = lambda x: 0, llambda: float = 0.1, sigma: float = 0.01):
        self.theta = theta
        self.llambda = llambda
        self.sigma = sigma  # sigma is always a float


    def eval_float_arg(self, r0: float, rng: Generator, dt: float):
        # cur_theta = self.theta
        # cur_theta_val = cur_theta(0)(r0)
        return (
                r0
                + self.llambda * (self.theta(0)(r0) + - r0) * dt
                + self.sigma * rng.standard_normal() * math.pow(dt, 0.5)
        )

    def eval_time_T_step_dt(self, T: float, dt: float, r_begin: float):
        num_timesteps = int(T / dt)
        rng = np.random.default_rng()
        return_value = [r_begin for _ in range(num_timesteps + 1)]
        for i in range(1, num_timesteps + 1):
            return_value[i] = self.eval_float_arg(return_value[i - 1], rng, dt)
        return return_value

    def eval_ZCB_price(self, t:float, T:float, llambda: float, P0: Callable, f0: Callable, r: Callable, frf: Callable) -> float:
        """Hull-White formula for P(t,T)."""
        tau = T - t
        ttheta = lambda x: 1 / llambda * frf(x) + f0(x) + self.sigma * self.sigma * (
                    1 - math.exp(-2 * llambda * x)) / (2 * llambda * llambda)
        B_func = lambda tau: -(math.exp(-llambda * tau) - 1) * 1.0 / llambda
        temp1 = llambda * sum(B_func(i*tau/100) * ttheta(T - i*tau/100) * (tau/100) for i in range(1,101))
        temp2 = (
                self.sigma * self.sigma / (4.0 * llambda * llambda * llambda)
                * (math.exp(-2.0*llambda*tau)*(4.0*math.exp(llambda*tau)-1.0)-3.0)
                + self.sigma * self.sigma * tau / (2.0 * llambda * llambda)
        )
        return_value = math.exp(temp1 + temp2)
        return return_value

    def eval_ZCB_price_works(self, t:float, T:float, a: float, P0: Callable, f0: Callable, r: Callable) -> float:
        """Hull-White formula for P(t,T)."""
        B = (1 - math.exp(-1/a * (T-t))) / a
        A = math.exp(
            math.log(P0(T) / P0(t))
            + f0(t) * B
            - 0.25 * self.sigma * self.sigma * ((math.exp(-1/a * T) - math.exp(-1/a * t))**2) * (math.exp(2 * 1/a * t) - 1) / (1/a * 1/a * 1/a)
        )
        # print(A, B, -r(t), A * math.exp(-r(t) * B))
        return A * math.exp(-r(t) * B)

    def eval_ZCB_price_old_2(self, t:float, T:float, a: float, P0: Callable, f0: Callable, r: Callable) -> float:
        """Hull-White formula for P(t,T)."""
        B = (1 - math.exp(-a * (T-t))) / a
        A = math.exp(
            math.log(P0(T) / P0(t))
            + f0(t) * (T - t)
            - 0.25 * self.sigma * self.sigma * ((math.exp(-a * T) - math.exp(-a * t))**2) * (math.exp(2 * a * t) - 1) / (a * a * a)
        )
        return A * math.exp(-r(t) * B)

    def eval_ZCB_price_old(self, t:float, T:float, a: float, P0: Callable, f0: Callable, r: Callable) -> float:
        """Hull-White formula for P(t,T)."""
        B = (1 - math.exp(-a * (T-t))) / a
        A = math.exp(
            math.log(P0(T) / P0(t))
            + f0(t) * (T - t)
            - 0.25 * self.sigma * self.sigma * ((math.exp(-a * T) - math.exp(-a * t))**2) * (math.exp(2 * a * t) - 1) / (a * a * a)
        )
        return A * math.exp(-r(t) * B)


if __name__=="__main__":
    pass