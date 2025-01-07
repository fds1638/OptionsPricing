import matplotlib.pyplot as plt
import math

def forward_euler(r, sigma, E, S_min, S_max, make_graph):
    """Convert Black Scholes to non-dimensional heat equation,
    and solve using forward Euler, following Wilmott."""

    # rescale to non-dimensional variables
    alpha = -1/2 * (2 * r / (sigma * sigma) - 1)
    beta = -1/4 * (2 * r / (sigma * sigma) + 1) * (2 * r / (sigma * sigma) + 1)
    Nminus = math.log(1/E)
    Nplus = math.log(S_max/E)
    x_mesh = 1000
    dx = (Nplus - Nminus)/x_mesh
    dt = 0.01 * dx * dx # extremely small timestep for accuracy

    x_values = [Nminus + dx * i for i in range(x_mesh +1)]

    # initial condition
    u_old = [ max(0, math.exp(-alpha * x_values[i]) * (math.exp(x_values[i]) - 1)) for i in range(x_mesh +1)]
    u = [None for i in range(x_mesh +1)]

    # option to graph
    if make_graph==1:
        plt.plot(x_values, u_old.copy())

    # solve using Forward Euler
    timestep_alpha = dt / (dx * dx)
    final_time = 0.025
    timestep_count = int(final_time/dt)
    for timestep in range(timestep_count + 1):
        u_min = 0
        tau = final_time / timestep_count * timestep
        u_max = math.exp(-alpha * Nplus) * math.exp(-beta * tau) * (math.exp(Nplus) - math.exp(-2*r/sigma/sigma*tau))
        for ii in range(0, len(u)):
            if ii==0:
                u[ii] = u_old[ii] + timestep_alpha * (
                    u_min - 2 * u_old[ii] + u_old[ii+1]
                )
            elif ii==len(u) - 1:
                u[ii] = u_old[ii] + timestep_alpha * (
                    u_old[ii-1] - 2 * u_old[ii] + u_max
                )
            else:
                u[ii] = u_old[ii] + timestep_alpha * (
                    u_old[ii-1] - 2 * u_old[ii] + u_old[ii+1]
                )
        u_old = u

    # option to graph
    if make_graph==1:
        plt.plot(x_values, u.copy())
        plt.legend(["u0", "u"])
        plt.show()

    # convert back to dimensional variables
    return_S = [E * math.exp(x_values[i]) for i in range(x_mesh +1)]
    return_V = [E * math.exp(alpha * x_values[i]) * u[i] * math.exp(beta * tau) for i in range(x_mesh +1)]
    return return_S, return_V

if __name__ == '__main__':
    """Example of forward Euler calculation."""
    S_max = 100
    S_min = 0
    E = 50
    sigma = 0.1
    r = 0.05

    # note for forward_euler plotting takes place in dimensionless variables
    forward_euler(r, sigma, E, S_min, S_max, 1)