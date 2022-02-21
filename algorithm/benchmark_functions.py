import numpy as np


def rosenbrock(x, y, a=1, b=100) -> float:
    """Benchmark function by Rosenbrock.

    Args:
        x (float): x-value
        y (float): y-value
        a (int, optional): Parameter of the Rosenbrock function. Defaults to 1.
        b (int, optional): Parameter of the Rosenbrock function. Defaults to 100.

    Returns:
        float: The calculated function value.
    """
    return (a - x) ** 2 + b * (y - x ** 2) ** 2


def rastrigin(x, y) -> float:
    """Benchmark function by Rastrigin.

    Args:
        x (float): x-value
        y (float): y-value

    Returns:
        float: The calculated function value.
    """
    return (x ** 2 - 10 * np.cos(2 * np.pi * x)) + (y ** 2 - 10 * np.cos(2 * np.pi * y)) + 20
