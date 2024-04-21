from config import *
from lsm_for_line import LeastSquaresMethodLine

import numpy as np
from matplotlib import pyplot as plt

a1, b1 = LeastSquaresMethodLine(x=np.log(t_k), y=np.log(k1)).get_solve()
a2, b2 = LeastSquaresMethodLine(x=np.log(t_k), y=np.log(k2)).get_solve()

# is_k1 = True
is_k1 = False

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

    return np.exp(a1 * np.log(t(_t)) + b1)


def k2(_t: int | float | np.ndarray):
    """
    Функция для получения значения второго варианта коэффициента поглощения
    в точках между узлами
    """

    return np.exp(a2 * np.log(t(_t)) + b2)


def der_u(z, _f):
    """
    Функция правой части первого уравнения
    f = f(z) - значение функции F в точке z
    """
    # мда, треш, долго доходило, что не k(z), а k(t(z))
    if is_k1:
        return -3 * r * k1(t(z)) / c * _f

    return -3 * r * k2(t(z)) / c * _f


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


def _lambda(z):
    """
    Функция λ(z)
    """
    if is_k1:
        c / (3 * k1(z))

    return c / (3 * k2(z))


def _p(z):
    """
    Функция p(z)
    """
    if is_k1:
        c * k1(z)

    return c * k2(z)


def f(z):
    """
    Функция f(z)
    """
    if is_k1:
        return c * k1(z) * u_p(z)

    return c * k2(z) * u_p(z)


def v_n(z, h):
    """
    Элемент объема
    """

    return ((z + h / 2) ** 2 - (z - h / 2) ** 2) / 2


def kappa1(z1, z2):
    """
    Функция каппа (вычисляется с использованием метода средних)
    """

    return (_lambda(z1) + _lambda(z2)) / 2


def kappa2(z1, z2):
    """
    Функция каппа (вычисляется с использованием метода трапеций)
    """

    return (2 * _lambda(z1) * _lambda(z2)) / (_lambda(z1) + _lambda(z2))


def left_boundary_condition(z0, g0, h):
    """
    Левое краевое условие метода правой прогонки
    """

    k0 = kappa1(z0, z0 + h) * (z0 + h / 2) / (r ** 2 * h) - _p(z0 + h / 2) * (z0 + h / 2) * h / 8  # правильно

    m0 = -kappa1(z0, z0 + h) * (z0 + h / 2) / (r ** 2 * h) - _p(z0 + h / 2) * (z0 + h / 2) * h / 8 - _p(z0) * z0 * h / 4

    p0 = -z0 * g0 / r - (f(z0 + h / 2) * (z0 + h / 2) + f(z0) * z0) * h / 4

    return k0, m0, p0


# При x = N
def right_boundary_condition(zn, h):
    """
    Правое краевое условие метода правой прогонки
    """
    kn = kappa1(zn - h, zn) * (zn - h / 2) / (r ** 2 * h) - _p(zn - h / 2) * (zn - h / 2) * h / 8  # правильно

    mn = -kappa1(zn - h, zn) * (zn - h / 2) / (r ** 2 * h) - 0.393 * c * zn / r - _p(zn) * zn * h / 4 - _p(
        zn - h / 2) * (zn - h / 2) * h / 8

    pn = -(f(zn) * zn + f(zn - h / 2) * (zn - h / 2)) * h / 4

    return kn, mn, pn


def right_sweep(a, b, h):
    """
    Реализация правой прогонки
    """

    # Прямой ход
    k0, m0, p0 = left_boundary_condition(a, 0, h)

    kn, mn, pn = right_boundary_condition(b, h)

    ksi = [0, -k0 / m0]
    eta = [0, p0 / m0]

    z = h
    n = 1

    while z < b + h / 2:
        a_n = (z - h / 2) * (kappa1(z - h, z)) / (r ** 2 * h)
        c_n = ((z + h / 2) * kappa1(z, z + h)) / (r ** 2 * h)
        b_n = a_n + c_n + _p(z) * v_n(z, h)
        d_n = f(z) * v_n(z, h)

        ksi.append(c_n / (b_n - a_n * ksi[n]))
        eta.append((a_n * eta[n] + d_n) / (b_n - a_n * ksi[n]))

        n += 1
        z += h

    # Обратный ход
    u = [0] * n

    u[n - 1] = (pn - kn * eta[n]) / (kn * ksi[n] + mn)

    for i in range(n - 2, -1, -1):
        u[i] = ksi[i + 1] * u[i + 1] + eta[i + 1]

    return u


def main() -> None:
    """
    Главная функция
    """
    a, b = 0, 1
    n = 1000  # число узлов
    h = (b - a) / n

    u_res = right_sweep(a, b, h)

    z_res = np.arange(a, b + h, h)

    up_res = [0] * len(z_res)

    for i in range(len(z_res)):
        up_res[i] = u_p(z_res[i])

    plt.subplot(2, 2, 1)
    plt.plot(z_res, u_res, 'r', label='u(z)')
    plt.plot(z_res, up_res, 'g', label='u_p')
    plt.legend()
    plt.grid()

    plt.show()


if __name__ == '__main__':
    main()
