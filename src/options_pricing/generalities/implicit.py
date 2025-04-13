import matplotlib.pyplot as plt
import math

def lu_find_y(y, timestep_alpha):
    '''Find y on main diagonal of U matrix.'''
    timestep_alpha_squared = timestep_alpha * timestep_alpha
    y[0] = 1 + 2 * timestep_alpha
    for i in range(1, len(y)):
        y[i] = (1 + 2 * timestep_alpha) - timestep_alpha_squared / y[i-1]
    return

def lu_solver(u, b, y, timestep_alpha, Nminus, Nplus):
    '''One timestep of LU decomposition.
    Must have run lu_find_y first to set up y.'''

    # solve Lq = b
    q = [None for _ in range(len(b))]
    q[0] = b[0]
    for n in range(1, len(q)):
        q[n] = b[n] + timestep_alpha * q[n-1] / y[n-1]

    # solve Uu = q
    u[-1] = q[-1] / y[-1]
    for n in range(len(u) - 2, -1, -1):
        u[n] = (q[n] + timestep_alpha * u[n+1]) / y[n]

    return

def backward_euler(r, sigma, E, S_min, S_max):
    """Convert Black Scholes to non-dimensional heat equation,
    and solve using backward Euler, following Wilmott."""

    # rescale to non-dimensional variables
    alpha = -1/2 * (2 * r / (sigma * sigma) - 1)
    beta = -1/4 * (2 * r / (sigma * sigma) + 1) * (2 * r / (sigma * sigma) + 1)
    Nminus = math.log(1/E)
    Nplus = math.log(S_max/E)
    x_mesh = 1000
    dx = (Nplus - Nminus)/x_mesh
    dt = 0.001
    timestep_alpha = dt / (dx * dx)

    # x domain
    x_values = [Nminus + dx * i for i in range(x_mesh +1)]

    # initial condition
    u0 = [ max(0, math.exp(-alpha * x_values[i]) * (math.exp(x_values[i]) - 1)) for i in range(x_mesh +1)]

    # set up y for LU decomposition
    y = [None for i in range(x_mesh + 1)]
    lu_find_y(y, timestep_alpha)

    # solve implicitly heat equation
    tau = 0
    u = u0
    final_time = 0.025
    timestep_count = int(final_time/dt)
    for timestep in range(timestep_count):
        b = u.copy()
        u_m_inf = 0
        tau = final_time / timestep_count * timestep
        u_p_inf = math.exp(-alpha * Nplus) * math.exp(-beta * tau) * (math.exp(Nplus) - math.exp(-2*r/sigma/sigma*tau))
        b[0] += timestep_alpha * u_m_inf
        b[-1] += timestep_alpha * u_p_inf
        lu_solver(u, b, y, timestep_alpha, Nminus, Nplus)

    # convert back to dimensional variables
    return_S = [E * math.exp(x_values[i]) for i in range(x_mesh +1)]
    return_V = [E * math.exp(alpha * x_values[i]) * u[i] * math.exp(beta * tau) for i in range(x_mesh +1)]
    return return_S, return_V

if __name__ == '__main__':
    """An example of a backward Euler calculation."""
    S_max = 100
    S_min = 0
    E = 50
    sigma = 0.1
    r = 0.05

    # plot initial condition
    plt.plot([i for i in range(0, 101)], [max(0, i - E) for i in range(0, 101)])

    # calculate using backward Euler with t = T - 5
    implicit_S, implicit_V = backward_euler(r, sigma, E, 0, 100)
    plt.plot(implicit_S, implicit_V)

    # plot
    plt.legend(["Backward Euler t=50=T", "Backward Euler t=45"])
    plt.show()
