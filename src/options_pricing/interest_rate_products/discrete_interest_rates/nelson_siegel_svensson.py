import math
import numpy as np
import scipy
from src.options_pricing.interest_rate_products.discrete_interest_rates.plot_handler import PlotHandler

class NelsonSiegelSvensson():

    def nelson_siegel_lambda(self, b0, b1, b2, ll):
        return lambda t: b0 + b1 * ((1 - math.exp(-ll*t))/(ll*t)) + b2 * ((1 - math.exp(-ll*t))/(ll*t) - math.exp(-ll*t))

    def nelson_siegel_svensson(self, b0, b1, b2, ll, t, b3, mu):
        return (
                b0
                + b1 * ((1 - math.exp(-ll * t)) / (ll * t))
                + b2 * ((1 - math.exp(-ll * t)) / (ll * t) - math.exp(-ll * t))
                + b3 * ((1 - math.exp(-mu * t)) / (mu * t) - math.exp(-mu * t))
        )

    def bondyield(self, b0, b1, b2, ll, t, b3, mu):
        return self.nelson_siegel_svensson(b0, b1, b2, ll, t, b3, mu)

    def value(self, b0, b1, b2, ll, t, coupons, b3, mu, pp=False):
        t_index = t - 1
        by = self.bondyield(b0, b1, b2, ll, t, b3, mu)
        # return 100 / math.pow(1+ by, t) + np.sum([coupons[t_index]/math.pow(1+by, tt) for tt in range(1, t+1)])
        yields = [self.bondyield(b0, b1, b2, ll, tt, b3, mu) for tt in range(1, t+1)]
        if pp:
            print("yields", yields)
            for ttt in range(1,t+1):
                print(ttt,yields[ttt-1])
        return 100 / math.pow(1+ by, t) + np.sum([coupons[t_index]/math.pow(1+yields[tt-1], tt) for tt in range(1, t+1)])

    def objective_function(self, coupons, bond_prices, ll, mu, b0, b1, b2, b3):
        return np.sum(
            [
                np.square(
                    bond_prices[t - 1] - self.value(b0,b1,b2,ll,t,coupons,b3,mu)
                ) for t in range(1,11)
            ]
        )


    def run_example(self):
        bond_prices = np.array([98.50,97.16,93.97,90.91,91.19,84.91,84.09,79.97,77.06,107.97])
        coupons = np.array([0.750,0.125,0.625,0.125,0.375,0.125,0.500,0.375,0.250,4.250])

        best_fit_error = 1000000000000000
        # choose bounds appropriate for given mu
        mu, bounds = 0.2, [(-1, 1),(-1, 1),(-1, 1),(-1, 1)]
        # mu, bounds = 0.5, [(-.5, .5),(-.5, .5),(-.5, .5),(-.5, .5)]
        for llambda_mult_100 in range(1,11):
            test_lambda = llambda_mult_100/100
            res = scipy.optimize.minimize(
                lambda coeffs: self.objective_function(coupons, bond_prices, test_lambda, mu, *coeffs),
                x0 = np.zeros(4),
                bounds = bounds
            )
            least_squares_error =                        self.objective_function(coupons, bond_prices, test_lambda, mu, *res.x)
            if least_squares_error < best_fit_error:
                best_fit_error = least_squares_error
                llambda = test_lambda
                beta0 = res.x[0]
                beta1 = res.x[1]
                beta2 = res.x[2]
                beta3 = res.x[3]

        print("Best fit params:")
        print("llambda", llambda)
        print("mu", mu)
        print("beta0", beta0)
        print("beta1", beta1)
        print("beta2", beta2)
        print("beta3", beta3)
        print("best_fit_error", best_fit_error)
        print()

        # for ttime in range(1,11):
        #     print("value", self.value(beta0, beta1, beta2, llambda, ttime, coupons, beta3, .2))


        plots = {}
        plot_t = [tt for tt in range(1,31)]
        plot_y = [self.bondyield(beta0, beta1, beta2, llambda, tt, beta3, mu) for tt in range(1,31)]
        plots["Nelson Siegel Svensson"] = (plot_t, plot_y)
        plothandler = PlotHandler()
        plothandler.make_plots(plots)



if __name__=="__main__":
    ns = NelsonSiegelSvensson()
    ns.run_example()
