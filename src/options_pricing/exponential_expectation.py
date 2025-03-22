import numpy as np
import math

def get_exponential_mean(n:int, mu:float, sigma:float) -> float:
    print(f"Create normal distribution ndarray of length {n} with average {mu:.5f} and std deviation {sigma:.5f}.")
    rng = np.random.default_rng()
    orig = rng.normal(mu, sigma, n)
    orig_avg = orig.mean()
    orig_st_dev = orig.std()
    print(f"Realized ndarray has average {orig_avg:.5f} and std deviation {orig_st_dev:.5f}.")
    print("Exponentiate each element of the array.")
    efunc = np.vectorize(lambda t: math.exp(t))
    expo = efunc(orig)
    print(f"This results in a realized lognormal ndarray with average {expo.mean():.5f} and std deviation {expo.std():.5f}.")
    print(f"Theoretically the lognormal ndarray should have average {math.exp(mu+0.5*sigma*sigma):.5f}")

if __name__=='__main__':
    '''Demonstration of expectation of a function of a random variable.'''
    get_exponential_mean(1000000, 2, 1)