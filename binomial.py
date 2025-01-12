import math

def get_payoff(derivative_type, stock, exercise):
    if derivative_type=="call":
        return max(0, stock - exercise)
    if derivative_type=="put":
        return max(0, exercise - stock)
    return 0

def get_binary_value(r, sigma, S, E, t, T, timesteps, deriv_type):
    dt = (T - t) / timesteps
    A = 0.5 * (math.exp(-r * dt) + math.exp((r + sigma * sigma) * dt))
    d = A - math.sqrt(A * A - 1)
    u = A + math.sqrt(A * A - 1)
    p = (math.exp(r * dt) - d) / (u - d)
    discount = math.exp(-r * dt)

    a = [None for _ in range(timesteps + 1)]
    a[0] = S

    for m in range(1, timesteps + 1):
        for n in range(m, 0, -1):
            a[n] = u * a[n - 1]
        a[0] = d * a[0]

    for n in range(len(a)):
        a[n] = get_payoff(deriv_type, a[n], E)

    for m in range(timesteps, 0 , -1):
        for n in range(m):
            a[n] = discount * (p * a[n + 1] + (1 - p) * a[n])

    return a[0]

if __name__ == '__main__':
    S = 60
    E = 50
    T = 50
    t = 45
    r = 0.05
    sigma = 0.1
    V = get_binary_value(r, sigma, S, E, t, T, 500)
    print("V", V)
