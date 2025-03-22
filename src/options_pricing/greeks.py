def delta(x_vector, y_vector):
    """Calc delta of function given, i.e. dy/dx."""
    # Assume x_vector and y_vector have same lengths.
    x_return = x_vector[1:len(x_vector) - 1]

    # Average forward and backward first difference
    y_return = []
    for i in range(1, len(x_vector) - 1):
        y_return.append(
                0.5 * (y_vector[i] - y_vector[i - 1]) / (x_vector[i] - x_vector[i - 1]) +
                0.5 * (y_vector[i + 1] - y_vector[i]) / (x_vector[i + 1] - x_vector[i])
        )
    return x_return, y_return
