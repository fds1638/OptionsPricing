import matplotlib.pyplot as plt
from scipy.optimize import fmin
import math

class NelsonSiegelSvensson():

    def __init__(self, b0=0.001, b1=0.01, b2=0.01, b3=0.01, l1=1.00, l2=2.00):
        self.b0 = b0
        self.b1 = b1
        self.b2 = b2
        self.b3 = b3
        self.l1 = l1
        self.l2 = l2

    def updateNSS(self, *args):
        pass

    def NSS(self, b0:float, b1:float, b2:float, b3:float, l1:float, l2:float, t:float) -> float:
        return (
            b0 +
            b1 * ((1 - math.exp(-l1 * t)) / (l1 * t)) +
            b2 * ((1 - math.exp(-l1 * t)) / (l1 * t) - math.exp(-l1 * t)) +
            b3 * ((1 - math.exp(-l2 * t)) / (l2 * t) - math.exp(-l2 * t))
        )

    # # not used, here to record previous attempt
    # def _minimization_value(self, NSS_params:list, yields_to_fit:list = [(1,0.0035), (2,0.0063), (5,.0181), (10, 0.0233), (20, 0.0349)])-> float:
    #     return sum(
    #         (self.NSS(NSS_params[0],NSS_params[1],NSS_params[2],NSS_params[3],NSS_params[4],NSS_params[5], yields_to_fit[i][0]) - yields_to_fit[i][1])**2
    #         for i in range(len(yields_to_fit))
    #     )
    # # not used, here to record previous attempt
    # def minimize_NSS(self) -> list[float]:
    #     return fmin(self._minimization_value, [self.b0, self.b1, self.b2, self.b3, self.l1, self.l2], maxiter=10000, maxfun=10000)


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

        return minimize_NSS

if __name__=="__main__":
    # below yields 21 March 2025 from home.treasury.gov
    yields_20250321 = [
        (1.0/12.0,4.36),(1.5/12.0,4.33),(2.0/12.0,4.33),(3.0/12.0,4.33),(4.0/12.0,4.29),(6.0/12.0,4.26),(1.0,4.04),(2.0,3.94),(3.0,3.92),(5.0,4.00),(7.0,4.12),(10.0,4.25),(20.0,4.60),(30.0,4.59)
    ]

    # get NSS fitting to above yields
    nss = NelsonSiegelSvensson()
    opt_func = nss.minimize_NSS_closure(yields_20250321)
    opt2 = opt_func()

    # plot
    legend = []
    plt.plot([yields_20250321[i][0] for i in range(len(yields_20250321))], [yields_20250321[i][1] for i in range(len(yields_20250321))],'o-')
    legend.append("yields 21 March 2025")
    plt.plot([yields_20250321[i][0] for i in range(len(yields_20250321))], [nss.NSS(opt2[0], opt2[1], opt2[2], opt2[3], opt2[4], opt2[5], yields_20250321[i][0]) for i in range(len(yields_20250321))],'o-')
    legend.append("closure approximation")
    plt.legend(legend)
    plt.show()
