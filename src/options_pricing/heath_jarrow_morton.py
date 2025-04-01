import matplotlib.pyplot as plt
from scipy.optimize import fmin
import math
import nelson_siegel_svensson
import ho_lee
from typing import Callable

class HeathJarrowMorton():
    def __init__(self, short_rate_model = "ho_lee"):
        self.short_rate_model = short_rate_model
        self.interest_rate_curve = []
        self.b0 = 0.1
        self.b1 = 0.1
        self.b2 = 0.1
        self.b3 = 0.1
        self.l1 = 1.0
        self.l2 = 1.0

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
    # plot
    hjm = HeathJarrowMorton()

    # yyy,aaa = hjm.get_interest_rate_curve()
    # legend = []
    # plt.plot([yyy[i][0] for i in range(len(yyy))], [yyy[i][1] for i in range(len(yyy))],'o-')
    # legend.append("yields 21 March 2025")
    # plt.plot([yyy[i][0] for i in range(len(yyy))], aaa,'o-')
    # legend.append("closure approximation")
    # plt.legend(legend)
    # plt.show()

    # hjm = HeathJarrowMorton()
    # times = [t / 48 for t in range(1, 30 * 48 + 1)]
    # forward_rates = hjm.get_forward_rate_curve(times)
    # plt.plot(times, forward_rates, 'o-')
    # plt.legend("times and forward rates")
    # plt.show()

    # sigma = 0.00001
    # sigma_contribution_to_theta = lambda x: sigma * sigma * x
    # frf = hjm.get_forward_rate_function()
    # theta = lambda x: hjm.get_forward_rate_function() #+ sigma_contribution_to_theta

    sigma = 0.005
    P = lambda t: math.exp(-0.04*t)
    f0 = lambda t: -(math.log(P(t + .1)) - math.log(P(t))) / 0.1
    frf = lambda T: (f0(T + .1) - f0(T - .1)) / 0.2 + sigma * sigma * T
    theta = lambda x: frf
    hl = ho_lee.HoLee(theta, sigma)

    print("f0(0)",f0(0))
    print("frf(0)", (f0(0 + .1) - f0(0 )) / 0.1 )
    time_values = [i/10 for i in range(1,101)]
    # interest_rates = hl.eval_time_T_step_dt(10, 0.1)

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


    averaged_results = []
    P_graph = []

    for i in range(len(time_values)):
        s = 0
        n = 0
        for j in range(number_of_runs):
            s += run_results[j][i]
            n += 1
        averaged_results.append(1.0*s/n)
        ms = 0
        mn = 0
        for j in range(number_of_runs):
            ms += 1.0/M_matrix[j][i]
            mn += 1
        P_graph.append(1.0*ms/mn)


    #
    # plt.plot(time_values, averaged_results,'o-')
    # plt.plot(time_values, run_results[23],'o-')


    # plt.plot(time_values, averaged_results,'o-')
    # plt.plot(time_values, run_results[154][1:],'o-')
    # plt.plot(time_values, run_results[454][1:],'o-')
    # plt.plot(time_values, run_results[554][1:],'o-')
    plt.plot(time_values, P_graph,'o-')
    plt.plot(time_values, [math.exp(-0.04*ti/10) for ti  in range(0,100)],'o-')
    # plt.plot(time_values, [1/M_matrix[264][ti] for ti  in range(1,101)],'o-')
    # plt.plot(time_values, [1/M_matrix[864][ti] for ti  in range(1,101)],'o-')
    # plt.plot(time_values, [1/M_matrix[824][ti] for ti  in range(1,101)],'o-')
    # plt.plot(time_values, [1/M_matrix[334][ti] for ti  in range(1,101)],'o-')
    # plt.plot(time_values, [1/M_matrix[777][ti] for ti  in range(1,101)],'o-')
    plt.legend("HJM")
    plt.show()

# return lambda t: (math.log(math.exp(-0.04 * t)) - math.log(math.exp(-0.04 * t + 0.1))) / 0.1
# return math.exp(-0.04 * t)
#
