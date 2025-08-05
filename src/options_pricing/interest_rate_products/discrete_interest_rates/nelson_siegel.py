import math
import numpy as np
import scipy
from plot_handler import PlotHandler

class NelsonSiegel():

    def nelson_siegel_lambda(self, b0, b1, b2, ll):
        return lambda t: b0 + b1 * ((1 - math.exp(-ll*t))/(ll*t)) + b2 * ((1 - math.exp(-ll*t))/(ll*t) - math.exp(-ll*t))

    def nelson_siegel(self, b0, b1, b2, ll, t):
        return b0 + b1 * ((1 - math.exp(-ll*t))/(ll*t)) + b2 * ((1 - math.exp(-ll*t))/(ll*t) - math.exp(-ll*t))

    def bondyield(self, b0, b1, b2, ll, t):
        return self.nelson_siegel(b0, b1, b2, ll, t)

    def value(self, b0, b1, b2, ll, t, coupons):
        t_index = t - 1
        by = self.bondyield(b0, b1, b2, ll, t)
        return 100 / math.pow(1+ by, t) + np.sum([coupons[t_index]/math.pow(1+by, tt) for tt in range(1, t+1)])

    def objective_function(self, coupons, bond_prices, ll, b0, b1, b2):
        return np.sum(
            [
                np.square(
                    bond_prices[t - 1] - self.value(b0,b1,b2,ll,t,coupons)
                ) for t in range(1,11)
            ]
        )


    def run_example(self):
        bond_prices = np.array([98.50,97.16,93.97,90.91,91.19,84.91,84.09,79.97,77.06,107.97])
        coupons = np.array([0.750,0.125,0.625,0.125,0.375,0.125,0.500,0.375,0.250,4.250])

        best_fit_error = 1000000000000000
        for llambda_mult_10 in range(1,101):
            test_lambda = llambda_mult_10/10
            res = scipy.optimize.minimize(lambda coeffs: self.objective_function(coupons, bond_prices, test_lambda, *coeffs), x0 = np.zeros(3))
            least_squares_error = self.objective_function(coupons, bond_prices, test_lambda, res.x[0], res.x[1], res.x[2])
            if least_squares_error < best_fit_error:
                best_fit_error = least_squares_error
                llambda = test_lambda
                beta0 = res.x[0]
                beta1 = res.x[1]
                beta2 = res.x[2]

        print("Best fit params:")
        print("llambda", llambda)
        print("beta0", beta0)
        print("beta1", beta1)
        print("beta2", beta2)
        print("best_fit_error", best_fit_error)
        print()



        print("value", self.value(beta0, beta1, beta2, llambda, 1, coupons))
        print("value", self.value(beta0, beta1, beta2, llambda, 2, coupons))
        print("value", self.value(beta0, beta1, beta2, llambda, 3, coupons))
        print("value", self.value(beta0, beta1, beta2, llambda, 4, coupons))
        print("value", self.value(beta0, beta1, beta2, llambda, 5, coupons))
        print("value", self.value(beta0, beta1, beta2, llambda, 6, coupons))
        print("value", self.value(beta0, beta1, beta2, llambda, 7, coupons))
        print("value", self.value(beta0, beta1, beta2, llambda, 8, coupons))
        print("value", self.value(beta0, beta1, beta2, llambda, 9, coupons))
        print("value", self.value(beta0, beta1, beta2, llambda, 10, coupons))
        print()
        print("objective_function", self.objective_function(coupons, bond_prices, llambda, beta0, beta1, beta2))
        print("beta0", beta0)
        print("beta1", beta1)
        print("beta2", beta2)

        plots = {}
        plot_t = [tt for tt in range(1,31)]
        plot_y = [self.bondyield(beta0, beta1, beta2, llambda, tt) for tt in range(1,31)]
        plots["Nelson Siegel"] = (plot_t, plot_y)
        plothandler = PlotHandler()
        plothandler.make_plots(plots)

if __name__=="__main__":
    ns = NelsonSiegel()
    ns.run_example()
