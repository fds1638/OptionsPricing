import matplotlib.pyplot as plt
from scipy.optimize import fmin
import math
import nelson_siegel_svensson
import ho_lee
from typing import Callable

class HeathJarrowMorton():
    def __init__(self, short_rate_model: str = "ho_lee", interest_rate_curve: str = "exponential"):
        self.short_rate_model = short_rate_model
        self.interest_rate_curve = interest_rate_curve
        self.interest_rate_curve_parameters = {
            "exponential": {
                "name": "exponential",
                "parameters": [0.4]
            },
            "nss": {
                "name": "nss",
                "parameters": [0.1, 0.1, 0.1, 0.1, 1.0, 1.0]
            }
        }
        self.yield_curve = []
        self.discount_curve = []
        self.T = 10
        self.dt = 0.1


    def get_yield_curve(self) -> None:
        if self.interest_rate_curve == "exponential":
            constant_r = self.interest_rate_curve_parameters["parameters"][0]
            num_timesteps = int(self.T/self.dt)
            self.yield_curve = list(constant_r for _ in range(num_timesteps))
        return

    def get_discount_curve(self) -> None:
        """From yield curve compute discount curve."""
        self.discount_curve = []
        self.discount_curve.append(1.0)
        for i in range(len(self.yield_curve)):
            self.discount_curve.append(
                self.discount_curve[-1] * math.exp(-1.0 * self.yield_curve[i] * self.dt)
            )
        return

    def graph_exponential_example(self) -> None:
        sigma = 0.005
        P = lambda t: math.exp(-0.04 * t)
        f0 = lambda t: -(math.log(P(t + .1)) - math.log(P(t))) / 0.1
        frf = lambda T: (f0(T + .1) - f0(T - .1)) / 0.2 + sigma * sigma * T
        theta = lambda x: frf
        hl = ho_lee.HoLee(theta, sigma)

        time_values = [i / 10 for i in range(1, 101)]

        # do a bunch of Ho-Lee simulations
        number_of_runs = 1000
        run_results = []
        M_matrix = []
        for _ in range(number_of_runs):
            interest_rates = hl.eval_time_T_step_dt(10, 0.1, f0(0))
            run_results.append(interest_rates.copy())
            M_matrix.append([1])
            for rr in range(len(interest_rates.copy()[1:])):
                last_value = M_matrix[-1][-1]
                M_matrix[-1].append(
                    last_value * math.exp((interest_rates.copy()[rr + 1] + interest_rates.copy()[rr]) * 0.5 * .1)
                )

        # average the simulations
        averaged_results = []
        P_graph = []

        for i in range(len(time_values)):
            s = 0
            n = 0
            for j in range(number_of_runs):
                s += run_results[j][i]
                n += 1
            averaged_results.append(1.0 * s / n)
            ms = 0
            mn = 0
            for j in range(number_of_runs):
                ms += 1.0 / M_matrix[j][i]
                mn += 1
            P_graph.append(1.0 * ms / mn)

        # plot average of simulations and show you reconstruct original P(t,T) discount curve
        plt.plot(time_values, P_graph, 'o-')
        plt.plot(time_values, [math.exp(-0.04 * ti / 10) for ti in range(0, 100)], 'o-')
        plt.legend("Original", "Ho-Lee Approximation")
        plt.show()

    def get_interest_rate_curve(self):
        nss = nelson_siegel_svensson.NelsonSiegelSvensson()
        yields = nss.get_interest_rates()
        opt_func = nss.minimize_NSS_closure(yields)
        opt2 = opt_func()
        self.b0, self.b1, self.b2, self.b3, self.l1, self.l2 = opt2[0], opt2[1], opt2[2], opt2[3], opt2[4], opt2[5]
        return yields, [nss.NSS(opt2[0], opt2[1], opt2[2], opt2[3], opt2[4], opt2[5], yields[i][0]) for i in
                  range(len(yields))]

    def get_forward_rate_function(self) -> Callable:
        # nss = nelson_siegel_svensson.NelsonSiegelSvensson()
        # yields = nss.get_interest_rates()
        # opt_func = nss.minimize_NSS_closure(yields)
        # opt2 = opt_func()
        # nss.updateNSS(opt2)
        # b0, b1, b2, b3, l1, l2 = opt2
        if self.interest_rate_curve == "exponential":
            b0, b1, b2, b3, l1, l2 = self.b0, self.b1, self.b2, self.b3, self.l1, self.l2
            return lambda t: 0.00 if t==0 else (-1.0 * (
                b1 * (math.exp(-l1 * t) / t - (1 - math.exp(-l1 * t)) / (l1 * t * t)) +
                b2 * (math.exp(-l1 * t) / t - (1 - math.exp(-l1 * t)) / (l1 * t * t) + l1 * math.exp(-l1 * t)) +
                b3 * (math.exp(-l2 * t) / t - (1 - math.exp(-l2 * t)) / (l2 * t * t) + l2 * math.exp(-l2 * t))
            ) / (
                b0 +
                b1 * ((1 - math.exp(-l1 * t)) / (l1 * t)) +
                b2 * ((1 - math.exp(-l1 * t)) / (l1 * t) - math.exp(-l1 * t)) +
                b3 * ((1 - math.exp(-l2 * t)) / (l2 * t) - math.exp(-l2 * t))
            )) + 0.001 * 0.001 * t


    def get_forward_rate_curve(self, time_array: list) -> list:
        nss = nelson_siegel_svensson.NelsonSiegelSvensson()
        yields = nss.get_interest_rates()
        opt_func = nss.minimize_NSS_closure(yields)
        opt2 = opt_func()
        nss.updateNSS(opt2)
        return nss.get_forward_rates(time_array)

    def get_short_rate(self):
        pass

if __name__=="__main__":
    hjm = HeathJarrowMorton()
    hjm.graph_exponential_example()

