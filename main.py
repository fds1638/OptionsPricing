import matplotlib.pyplot as plt
import numpy as np
from Black_Scholes_closed_form_02 import BlackScholesCallValue
from forward_euler import forward_euler
from implicit import backward_euler

if __name__ == '__main__':
    # stock and option parameters
    sigma = 0.1 # volatility
    r = 0.05    # risk-free interest rate
    E = 50      # exercise price

    # exact solution
    S_values = np.linspace(1, 100, 990)
    t_values = [45, 50]
    for t in t_values:
        plt.plot(S_values, BlackScholesCallValue(S_values, 0, t, 50, 50, sigma, r))

    # forward euler solution
    heat_S, heat_V = forward_euler(r, sigma, E, 0, 100, 0)
    plt.plot(heat_S, heat_V)

    # backward euler solution
    implicit_S, implicit_V = backward_euler(r, sigma, E, 0, 100)
    plt.plot(implicit_S, implicit_V)

    # plot
    plt.legend(["Exact t=" + str(t_value) for t_value in t_values] + ["FE t=45"] + ["BE t=45"])
    plt.show()


