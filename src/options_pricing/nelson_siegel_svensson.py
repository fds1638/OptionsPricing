import matplotlib.pyplot as plt
from scipy.optimize import fmin
import math
from importlib import resources
from typing import Callable

class NelsonSiegelSvensson():

    def __init__(self, b0=0.001, b1=0.01, b2=0.01, b3=0.01, l1=1.00, l2=2.00):
        self.b0 = b0
        self.b1 = b1
        self.b2 = b2
        self.b3 = b3
        self.l1 = l1
        self.l2 = l2

    def updateNSS(self, args) -> None:
        self.b0 = args[0]
        self.b1 = args[1]
        self.b2 = args[2]
        self.b3 = args[3]
        self.l1 = args[4]
        self.l2 = args[5]
        return

    def get_interest_rates(self):
        return_value = []
        ref = resources.files("interest_rates") / "yields_20250321"
        with open(ref, "r") as f:
            for line in f:
                line_array = line.strip().split(",")
                return_value.append((float(line_array[0]),float(line_array[1])))
        return return_value

    def get_first_derivative(self, b0:float, b1:float, b2:float, b3:float, l1:float, l2:float, t:float) -> float:
        return (
            b1 * (math.exp(-l1 * t) / t - (1 - math.exp(-l1 * t)) / (l1 * t * t)) +
            b2 * (math.exp(-l1 * t) / t - (1 - math.exp(-l1 * t)) / (l1 * t * t) + l1 * math.exp(-l1 * t)) +
            b3 * (math.exp(-l2 * t) / t - (1 - math.exp(-l2 * t)) / (l2 * t * t) + l2 * math.exp(-l2 * t))
        )

    def get_forward_rate(self, t:float) -> float:
        return (
            -1.0 *
            self.get_first_derivative(self.b0, self.b1, self.b2, self.b3, self.l1, self.l2, t) /
            self.NSS(self.b0, self.b1, self.b2, self.b3, self.l1, self.l2, t)
        )

    def misc(self, sigma:float) -> Callable:
        return lambda x: sigma * sigma * x
    def get_forward_rate_function(self) -> Callable:
        return -1.0 * self.get_first_derivative / self.NSS + self.misc
    def get_forward_rates(self, time_array:list) -> list:
        return list(
            self.get_forward_rate(time_array[ii]) for ii in range(len(time_array))
        )
    def NSS(self, b0:float, b1:float, b2:float, b3:float, l1:float, l2:float, t:float) -> float:
        return (
            b0 +
            b1 * ((1 - math.exp(-l1 * t)) / (l1 * t)) +
            b2 * ((1 - math.exp(-l1 * t)) / (l1 * t) - math.exp(-l1 * t)) +
            b3 * ((1 - math.exp(-l2 * t)) / (l2 * t) - math.exp(-l2 * t))
        )

    # Used a closure in order to be able to pass different yield_to_fit lists to _minimization_value.
    def minimize_NSS_closure(self, yield_to_fit):
        def minimize_NSS() -> list[float]:
            def _minimization_value(NSS_params: list) -> float:
                return sum(
                    (self.NSS(NSS_params[0], NSS_params[1], NSS_params[2], NSS_params[3], NSS_params[4], NSS_params[5],
                              yield_to_fit[i][0]) - yield_to_fit[i][1]) ** 2
                    for i in range(len(yield_to_fit))
                )

            return fmin(_minimization_value, [self.b0, self.b1, self.b2, self.b3, self.l1, self.l2], maxiter=100000, maxfun=100000)
        # print("minimize_NSS", minimize_NSS())
        return minimize_NSS

if __name__=="__main__":
    nss = NelsonSiegelSvensson()
    yields_20250321 = nss.get_interest_rates()     # yields 21 March 2025 from home.treasury.gov
    opt_func = nss.minimize_NSS_closure(yields_20250321)
    opt2 = opt_func()
    nss.updateNSS(opt2)

    # plot
    legend = []
    plt.plot([yields_20250321[i][0] for i in range(len(yields_20250321))], [yields_20250321[i][1] for i in range(len(yields_20250321))],'o-')
    legend.append("yields 21 March 2025")
    plt.plot([yields_20250321[i][0] for i in range(len(yields_20250321))], [nss.NSS(opt2[0], opt2[1], opt2[2], opt2[3], opt2[4], opt2[5], yields_20250321[i][0]) for i in range(len(yields_20250321))],'o-')
    legend.append("closure approximation")
    plt.legend(legend)
    plt.show()

    # plot
    times = [t/48 for t in range(1,30*48+1)]
    forward_rates = nss.get_forward_rates(times)
    plt.plot(times, forward_rates,'o-')
    plt.legend("times and forward rates")
    plt.show()
