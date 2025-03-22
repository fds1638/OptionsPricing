import matplotlib.pyplot as plt
import numpy as np
from src.options_pricing.Black_Scholes_closed_form_02 import BlackScholesPutValue, BlackScholesCallValue
from src.options_pricing.forward_euler import forward_euler

if __name__ == '__main__':
    """Compute value of straddle exactly and using backward and forward Euler."""
    # stock and option parameters
    sigma = 0.1 # volatility
    r = 0.02    # risk-free interest rate
    E = 50      # exercise price

    # exact solution
    S_values = np.linspace(1, 100, 990)
    t_values = [45, 50]
    call_values = None
    for t in t_values:
        call_values_t = BlackScholesCallValue(S_values, 0, t, 50, 50, sigma, r)
        put_values_t = BlackScholesPutValue(S_values, 0, t, 50, 50, sigma, r)
        straddle_values_t = [call_values_t[ii] + put_values_t[ii] for ii in range(len(call_values_t))]
        plt.plot(S_values, straddle_values_t)
        if t == 45:
            call_values = call_values_t.copy()

    # forward euler solution
    heat_S, heat_V = forward_euler(r, sigma, E, 0, 100, 0, "straddle")
    plt.plot(heat_S, heat_V)

    # # backward euler solution
    # implicit_S, implicit_V = backward_euler(r, sigma, E, 0, 100)
    # plt.plot(implicit_S, implicit_V)
    #
    # # binomial tree solution
    # bin_S = [i for i in range(1, 2 * E + 1)]
    # bin_V = []
    # for ii in range(len(bin_S)):
    #     bin_V.append(
    #         get_binary_value(r, sigma, bin_S[ii], E, 45, 50, 500, "call")
    #     )
    # plt.plot(bin_S, bin_V)

    # plot
    plt.legend(["Exact t=" + str(t_value) for t_value in t_values] + ["FE t=45"] + ["BE t=45"] + ["binomial t=45"])
    plt.show()



    # S = 60
    # E = 50
    # T = 50
    # t = 45
    # r = 0.05
    # sigma = 0.1
    # V = get_binary_value(r, sigma, S, E, t, T, 500)
    # print("V", V)
