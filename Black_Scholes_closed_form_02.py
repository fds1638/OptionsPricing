import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.stats import norm

def gaussian(x, mu, sigma):
    return (
        1.0 / (np.sqrt(2.0 * np.pi) * sigma) * np.exp(-np.power((x - mu) / sigma, 2.0) / 2)
    )

def BlackScholesCallValue(S_array, D, t, T, E, sigma, r):
    """Closed form Black Scholes value for a call, following Wilmott."""
    retval = []
    for S in S_array:
        if T - t > 0:
            d1 = (math.log(S/E) + (r - D + 1/2 * sigma * sigma)*(T - t)) / (sigma * math.sqrt(T - t))
            d2 = d1 - sigma * math.sqrt(T - t)
            retval.append(S * math.exp(-D * (T - t)) * norm.cdf(d1) - E * math.exp(-r * (T - t)) * norm.cdf(d2))
        else:
            retval.append(max(0, S - E))
    return retval

if __name__ == '__main__':
    """Black Scholes closed form example, following Wilmott."""

    # Stock price ranges from 1 to 100, volatility is 0.1. Expiry time is T = 50. Choose a few values for time t <= 50.
    sigma = 0.1
    S_values = np.linspace(1, 100, 990)
    t_values = [30, 40, 45, 49, 50]
    for t in t_values:
        plt.plot(S_values, BlackScholesCallValue(S_values, 0, t, 50, 50, sigma, 0.05))
    plt.legend(t_values)
    plt.show()
