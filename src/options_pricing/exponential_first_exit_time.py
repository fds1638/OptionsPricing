import matplotlib.pyplot as plt
import numpy as np
import math

def get_exponential_time_leave_range(S:float, mu:float, sigma:float, S0:float, S1:float) -> float:
    '''Function which gives expected exit time of geometric Brownian motion from range.
    S = current asset price
    mu = drift
    sigma = volatility
    S0 = lower end of range
    S1 = upper end of range'''
    return (
        1.0 / (0.5*sigma*sigma - mu)
        * (math.log(S/S0) - (1-math.pow(S/S0,1-2*mu/sigma/sigma))/(1-math.pow(S1/S0,1-2*mu/sigma/sigma)) * math.log(S1/S0))
    )

def get_exponential_time_leave_range_array(S_values:np.linspace, mu:float, sigma:float, S0:float, S1:float) -> float:
    return [get_exponential_time_leave_range(S, mu, sigma, S0, S1) for S in S_values]

if __name__=='__main__':
    S0 = 10
    S1 = 40
    sigma = 0.05
    S_values = np.linspace(S0, S1, 100)
    legend = []
    for mu in [-0.05, 0.0, 0.02]:
        result_vector = get_exponential_time_leave_range_array(S_values, mu, sigma, S0, S1)
        plt.plot(S_values, result_vector.copy())
        legend.append(f"mu={mu}, sigma={sigma}")
    plt.legend(legend)
    plt.show()
