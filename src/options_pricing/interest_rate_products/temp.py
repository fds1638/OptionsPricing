import matplotlib.pyplot as plt
import math
from src.options_pricing.interest_rate_products import ho_lee, hull_white, nelson_siegel_svensson
from typing import Callable

class HeathJarrowMorton():
    def __init__(self, short_rate_model: str = "ho_lee", interest_rate_curve: str = "exponential"):
        self.short_rate_model = short_rate_model
        self.interest_rate_curve = interest_rate_curve
        self.interest_rate_curve_parameters = {
            "exponential": {
                "name": "exponential",
                "parameters": [0.04]
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
        self.sigma = 0.01
        self.number_of_runs = 1000

    def set_yield_curve(self) -> None:
        """Populate self.yield_curve."""
        self.yield_curve = []
        if self.interest_rate_curve == "exponential":
            constant_r = self.interest_rate_curve_parameters["parameters"][0]
            num_timesteps = int(self.T/self.dt)
            self.yield_curve = list(constant_r for _ in range(num_timesteps))
        return

    def set_discount_curve(self) -> None:
        """From self.yield curve compute self.discount_curve."""
        self.discount_curve = []
        self.discount_curve.append(1.0)
        for i in range(len(self.yield_curve)):
            self.discount_curve.append(
                self.discount_curve[-1] * math.exp(-1.0 * self.yield_curve[i] * self.dt)
            )
        return

    def run_simulations(self, number_of_runs: int, short_rate_model, f0: Callable):
        """Given Ho-Lee / Hull-White and forward function f0 = f(0,T), return interest rates and size of Money savings account."""
        run_results_retval = []
        M_matrix_retval = []
        for _ in range(number_of_runs):
            interest_rates = short_rate_model.eval_time_T_step_dt(10, 0.1, f0(0))
            run_results_retval.append(interest_rates.copy())
            M_matrix_retval.append([1])
            for rr in range(len(interest_rates.copy()[1:])):
                last_value = M_matrix_retval[-1][-1]
                M_matrix_retval[-1].append(
                    last_value * math.exp((interest_rates.copy()[rr + 1] + interest_rates.copy()[rr]) * 0.5 * .1)
                )
        return run_results_retval, M_matrix_retval

    def average_simulations(self, number_of_runs, time_values, simulation_run_results, simulation_M_matrix):
        """Average Ho-Lee / Hull-White results for interest rate and for Money savings account growth."""
        averaged_results_retval = []
        P_graph_retval = []
        for i in range(len(time_values)):
            s = 0
            ms = 0
            n = 0
            for j in range(number_of_runs):
                s += simulation_run_results[j][i]
                ms += 1.0 / simulation_M_matrix[j][i]
                n += 1
            averaged_results_retval.append(1.0 * s / n)
            P_graph_retval.append(1.0 * ms / n)
        return averaged_results_retval, P_graph_retval

    def plot_graph(self, time_values, P_graph):
        """Create plots."""
        plt.plot(time_values, P_graph, 'o-')
        plt.plot(time_values, [
            math.exp(-self.interest_rate_curve_parameters[self.interest_rate_curve]["parameters"][0] * ti * self.dt) for
            ti in range(0, 100)])
        plt.legend(["Original", "Ho-Lee Approximation"])
        plt.show()

    def graph_exponential_example(self) -> None:
        """Show reconstruction of exponential ZCB (i.e. discount) curve
        with Ho-Lee or Hull-White short term model."""
        if self.short_rate_model == "ho_lee":
            # Get functions and parameters.
            P = lambda t: math.exp(-self.interest_rate_curve_parameters[self.interest_rate_curve]["parameters"][0] * t)
            f0 = lambda t: -(math.log(P(t + self.dt)) - math.log(P(t))) / self.dt
            frf = lambda T: (f0(T + self.dt) - f0(T - self.dt)) / (2 * self.dt) + self.sigma * self.sigma * T
            theta = lambda x: frf
            # hl = ho_lee.HoLee(theta, self.sigma)
            hl = ho_lee.HoLee.create(theta, self.sigma)

            # Do a bunch of Ho-Lee simulations for interest rates and for Money savings account value.
            run_results, M_matrix = self.run_simulations(self.number_of_runs, hl, f0)

            # Average the simulations.
            time_values = [self.dt * i for i in range(1, 101)]
            averaged_results, P_graph = self.average_simulations(self.number_of_runs, time_values, run_results, M_matrix)

            # plot average of simulations and show you reconstruct original P(t,T) discount curve
            self.plot_graph(time_values, P_graph)

        elif self.short_rate_model == "hull_white":
            # Get functions and parameters.
            P = lambda t: math.exp(-self.interest_rate_curve_parameters[self.interest_rate_curve]["parameters"][0] * t)
            f0 = lambda t: -(math.log(P(t + self.dt)) - math.log(P(t))) / self.dt
            frf = lambda T: (f0(T + self.dt) - f0(T - self.dt)) / (2 * self.dt) + self.sigma * self.sigma * T
            llambda = 0.5
            theta_pre = lambda x: 1/llambda * frf(x) + f0(x) + self.sigma * self.sigma * (1 - math.exp(-2 * llambda * x)) / (2 * llambda * llambda)
            theta = lambda x: theta_pre
            hw = hull_white.HullWhiteFunction(theta, llambda, self.sigma)
            # hl = hull_white.Hu.create(theta, self.sigma)

            # Do a bunch of Ho-Lee simulations for interest rates and for Money savings account value.
            run_results, M_matrix = self.run_simulations(self.number_of_runs, hw, f0)

            # Average the simulations.
            time_values = [self.dt * i for i in range(1, 101)]
            averaged_results, P_graph = self.average_simulations(self.number_of_runs, time_values, run_results, M_matrix)

            # plot average of simulations and show you reconstruct original P(t,T) discount curve
            self.plot_graph(time_values, P_graph)


    def integral_0_to_t(self, f: Callable, t: float):
        print("t", t, "self.dt", self.dt, "int(t/(self.dt/10))", int(t/(self.dt/10)))
        retval = sum(
            (f(tt + 1) * (self.dt/10)) for tt in range(int(t/(self.dt/10)))
        )
        print("retval", retval)
        return retval

    def graph_20250321_example(self) -> None:
        # Get functions and parameters.
        nss = nelson_siegel_svensson.NelsonSiegelSvensson()
        yields_20250321 = nss.get_interest_rates()  # yields 21 March 2025 from home.treasury.gov
        opt_func = nss.minimize_NSS_closure(yields_20250321)
        opt2 = opt_func()
        b0, b1, b2, b3, l1, l2 = opt2[0], opt2[1], opt2[2], opt2[3], opt2[4], opt2[5]
        print(b0, b1, b2, b3, l1, l2)
        opt2_func = (lambda t:
                     (
                         b0 +
                         b1 * ((1 - math.exp(-l1 * t)) / (l1 * t)) +
                         b2 * ((1 - math.exp(-l1 * t)) / (l1 * t) - math.exp(-l1 * t)) +
                         b3 * ((1 - math.exp(-l2 * t)) / (l2 * t) - math.exp(-l2 * t))
                      ) / 100 # divide by 100 to go from percent to decimal
                     )
        #        print(opt2_func(0.0))
        time_values = [self.dt * i for i in range(1, 101)]
        opt2_vec = list(opt2_func(i * self.dt) for i in range(1,101))
        plt.plot(time_values, opt2_vec, 'o-')
        plt.legend(["opt2_vec"])
        plt.show()
        P = lambda t: math.exp(-self.integral_0_to_t(opt2_func, t))
        P_vec = list(P(i * self.dt) for i in range(0,100))
        print("P_vec", P_vec)
        plt.plot(time_values, P_vec, 'o-')
        plt.legend(["P_vec"])
        plt.show()
        f0 = lambda t: -(math.log(P(t + self.dt)) - math.log(P(t))) / self.dt
        f0_vec = list(f0(i * self.dt) for i in range(0,100))
        f0_vec = list(-(P_vec[i] - P_vec[i-1])/self.dt for i in range(1, len(P_vec)))
        print("f0_vec", f0_vec)
        plt.plot(time_values[:-1], f0_vec, 'o-')
        plt.legend(["f0_vec"])
        plt.show()
        frf = lambda T: (f0(T + self.dt) - f0(T - self.dt)) / (2 * self.dt) + self.sigma * self.sigma * T
        frf_vec = list((f0_vec[i] - f0_vec[i-1])/self.dt + self.sigma * self.sigma * (i-1) * self.dt for i in range(1, len(f0_vec)))
        print("frf_vec", frf_vec)
        plt.plot(time_values[:-2], frf_vec, 'o-')
        plt.legend(["frf_vec"])
        plt.show()
        theta = lambda x: frf
        theta_vec = frf_vec.copy()
        # hl = ho_lee.HoLee(theta, self.sigma)

        hl = ho_lee.HoLee.create(theta_vec, self.sigma)
        run_results = []
        M_matrix = []
        number_of_runs = 1000
        for _ in range(number_of_runs):
            interest_rates = hl.eval_theta_list(frf_vec[0], 0.1, theta_vec)
            run_results.append(interest_rates.copy())
            M_matrix.append([1])
            for rr in range(len(interest_rates.copy()[1:])):
                last_value = M_matrix[-1][-1]
                M_matrix[-1].append(
                    last_value * math.exp((interest_rates.copy()[rr + 1] + interest_rates.copy()[rr]) * 0.5 * .1)
                )

        averaged_results = []
        P_graph = []
        for i in range(len(run_results[0])):
            s = 0
            ms = 0
            n = 0
            for j in range(number_of_runs):
                s += run_results[j][i]
                ms += 1.0 / M_matrix[j][i]
                n += 1
            averaged_results.append(1.0 * s / n)
            P_graph.append(1.0 * ms / n)

        plt.plot(time_values[:-1], P_graph, 'o-')
        plt.plot(time_values, P_vec, '-')
        plt.legend(["Ho-Lee Vector Approximation", "Original"])
        plt.show()
        return

        # Do a bunch of Ho-Lee simulations for interest rates and for Money savings account value.
        run_results, M_matrix = self.run_ho_lee_simulations(self.number_of_runs, hl, f0)

        # Average the simulations.
        time_values = [self.dt * i for i in range(1, 101)]
        averaged_results, P_graph = self.average_ho_lee_simulations(number_of_runs, time_values, run_results,
                                                                    M_matrix)

        # plot average of simulations and show you reconstruct original P(t,T) discount curve
        self.plot_graph(time_values, P_graph)

    # def graph_20250321_example(self) -> None:
    #     # Get functions and parameters.
    #     nss = nelson_siegel_svensson.NelsonSiegelSvensson()
    #     yields_20250321 = nss.get_interest_rates()  # yields 21 March 2025 from home.treasury.gov
    #     opt_func = nss.minimize_NSS_closure(yields_20250321)
    #     opt2 = opt_func()
    #     b0, b1, b2, b3, l1, l2 = opt2[0], opt2[1], opt2[2], opt2[3], opt2[4], opt2[5]
    #     print(b0, b1, b2, b3, l1, l2)
    #     opt2_func = (lambda t:
    #                  b0 +
    #                  b1 * ((1 - math.exp(-l1 * t)) / (l1 * t)) +
    #                  b2 * ((1 - math.exp(-l1 * t)) / (l1 * t) - math.exp(-l1 * t)) +
    #                  b3 * ((1 - math.exp(-l2 * t)) / (l2 * t) - math.exp(-l2 * t))
    #                  )
    #     #        print(opt2_func(0.0))
    #     nss.updateNSS(opt2)
    #     P = lambda t: math.exp(-self.integral_0_to_t(opt2_func, t))
    #     f0 = lambda t: -(math.log(P(t + self.dt)) - math.log(P(t))) / self.dt
    #     frf = lambda T: (f0(T + self.dt) - f0(T - self.dt)) / (2 * self.dt) + self.sigma * self.sigma * T
    #     theta = lambda x: frf
    #     # hl = ho_lee.HoLee(theta, self.sigma)
    #     hl = ho_lee.HoLee.create(theta, self.sigma)
    #
    #     # Do a bunch of Ho-Lee simulations for interest rates and for Money savings account value.
    #     run_results, M_matrix = self.run_ho_lee_simulations(self.number_of_runs, hl, f0)
    #
    #     # Average the simulations.
    #     time_values = [self.dt * i for i in range(1, 101)]
    #     averaged_results, P_graph = self.average_ho_lee_simulations(number_of_runs, time_values, run_results,
    #                                                                 M_matrix)
    #
    #     # plot average of simulations and show you reconstruct original P(t,T) discount curve
    #     self.plot_graph(time_values, P_graph)

    # def get_interest_rate_curve(self):
    #     nss = nelson_siegel_svensson.NelsonSiegelSvensson()
    #     yields = nss.get_interest_rates()
    #     opt_func = nss.minimize_NSS_closure(yields)
    #     opt2 = opt_func()
    #     self.b0, self.b1, self.b2, self.b3, self.l1, self.l2 = opt2[0], opt2[1], opt2[2], opt2[3], opt2[4], opt2[5]
    #     return yields, [nss.NSS(opt2[0], opt2[1], opt2[2], opt2[3], opt2[4], opt2[5], yields[i][0]) for i in
    #               range(len(yields))]

    # def get_forward_rate_function(self) -> Callable:
    #     # nss = nelson_siegel_svensson.NelsonSiegelSvensson()
    #     # yields = nss.get_interest_rates()
    #     # opt_func = nss.minimize_NSS_closure(yields)
    #     # opt2 = opt_func()
    #     # nss.updateNSS(opt2)
    #     # b0, b1, b2, b3, l1, l2 = opt2
    #     if self.interest_rate_curve == "exponential":
    #         b0, b1, b2, b3, l1, l2 = self.b0, self.b1, self.b2, self.b3, self.l1, self.l2
    #         return lambda t: 0.00 if t==0 else (-1.0 * (
    #             b1 * (math.exp(-l1 * t) / t - (1 - math.exp(-l1 * t)) / (l1 * t * t)) +
    #             b2 * (math.exp(-l1 * t) / t - (1 - math.exp(-l1 * t)) / (l1 * t * t) + l1 * math.exp(-l1 * t)) +
    #             b3 * (math.exp(-l2 * t) / t - (1 - math.exp(-l2 * t)) / (l2 * t * t) + l2 * math.exp(-l2 * t))
    #         ) / (
    #             b0 +
    #             b1 * ((1 - math.exp(-l1 * t)) / (l1 * t)) +
    #             b2 * ((1 - math.exp(-l1 * t)) / (l1 * t) - math.exp(-l1 * t)) +
    #             b3 * ((1 - math.exp(-l2 * t)) / (l2 * t) - math.exp(-l2 * t))
    #         )) + 0.001 * 0.001 * t
    #

    # def get_forward_rate_curve(self, time_array: list) -> list:
    #     nss = nelson_siegel_svensson.NelsonSiegelSvensson()
    #     yields = nss.get_interest_rates()
    #     opt_func = nss.minimize_NSS_closure(yields)
    #     opt2 = opt_func()
    #     nss.updateNSS(opt2)
    #     return nss.get_forward_rates(time_array)

if __name__=="__main__":
    """Yield curve is level, exponential discount curve. Show that HJM+HL reconstructs discount curve."""
    hjm = HeathJarrowMorton()
    hjm.graph_exponential_example()
    del(hjm)
    # hjm = HeathJarrowMorton()
    # hjm.graph_20250321_example()
    # del(hjm)
    # hjm = HeathJarrowMorton()
    # hjm.graph_exponential_example_hullwhite()
    # del(hjm)
    hjm = HeathJarrowMorton("hull_white")
    hjm.graph_exponential_example()
    del(hjm)


