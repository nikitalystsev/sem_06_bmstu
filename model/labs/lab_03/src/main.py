from config import *
from lsm_for_line import LeastSquaresMethodLine

import numpy as np
from scipy import integrate
from matplotlib import pyplot as plt

a1, b1 = LeastSquaresMethodLine(x=t_k, y=k1).get_solve()
a2, b2 = LeastSquaresMethodLine(x=t_k, y=k2).get_solve()

is_k1 = True
# is_k1 = False

EPS = 1e-4


def t(z: int | float | np.ndarray):
    """
    T(z)- температурное поле в цилиндре.
    """

    return (t_w - t_0) * z ** p + t_0


def u_p(z: int | float | np.ndarray):
    """
    Функция Планка
    """

    return 3.084e-4 / (np.exp(4.799e4 / t(z)) - 1)


def k1(_t: int | float | np.ndarray):
    """
    Функция для получения значения первого варианта коэффициента поглощения
    в точках между узлами
    """

    return np.exp(a1 * np.log(_t) + b1)


def k2(_t: int | float | np.ndarray):
    """
    Функция для получения значения второго варианта коэффициента поглощения
    в точках между узлами
    """

    return np.exp(a2 * np.log(_t) + b2)


def der_u(z, f):
    """
    Функция правой части первого уравнения
    f = f(z) - значение функции F в точке z
    """
    # мда, треш, долго доходило, что не k(z), а k(t(z))
    if is_k1:
        return -3 * r * k1(t(z)) / c * f

    return -3 * r * k2(t(z)) / c * f


def der_f(z, u, _f):
    """
    Функция правой части первого уравнения
    f = f(z) - значение функции F в точке z
    u = u(z) - значение функции u в точке z
    """
    if is_k1:
        common_part = r * c * k1(t(z)) * (u_p(z) - u)
    else:
        common_part = r * c * k2(t(z)) * (u_p(z) - u)

    res = -_f / z + common_part if abs(z) > EPS else common_part / 2

    return res


def f(z, s):
    """
    Для передачи ее в мат. пакет
    """
    dudz = der_u(z, s[1])
    dfdz = der_f(z, s[0], s[1])

    return [dudz, dfdz]


def boundary_residual(ya, yb):
    return np.array([
        ya[0] - 0,
        yb[0] - 1
    ])


def main() -> None:
    """
    Главная функция
    """
    a, b = 0, 1
    n = 50
    h = (b - a) / n

    z = np.arange(a, b + h, h)

    y_guess = np.zeros((2, n + 1), dtype=float)

    sol = integrate.solve_bvp(f, boundary_residual, z, y_guess)

    fig, ax = plt.subplots(figsize=(8, 8), layout="tight")

    ax.plot(z, sol.y, label="u(z)")


if __name__ == '__main__':
    main()
