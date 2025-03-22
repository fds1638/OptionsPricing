import matplotlib.pyplot as plt
import numpy as np
import statistics

def brownian_until_hit(init:float, barrier: float, mu:float, sigma:float, cutoff:int) -> int:
    y = init
    t = 0
    rng = np.random.default_rng()
    while y < barrier and t < cutoff:
        y = y + mu + sigma * rng.standard_normal()
        t += 1
    return t


if __name__=='__main__':
    mu = 0
    sigma = 0.05
    barrier = 1
    x0=0
    cutoff = 10001

    stopping_times = []
    for i in range(1000):
        latest_time = brownian_until_hit(x0, barrier, mu, sigma, cutoff)
        stopping_times.append(latest_time)
    print("simulations done")
    mean_st = statistics.mean(stopping_times)
    print("mean stopping time",mean_st)
    median_st = statistics.median(stopping_times)
    print("median stopping time",median_st)

    t_values = [10*i for i in range(1000)]
    plt.hist(stopping_times, bins=t_values)
    plt.title(f"Hitting time:\n mu={mu}, sigma={sigma}, barrier={barrier}, mean={mean_st}, median={median_st}")
    plt.show()

