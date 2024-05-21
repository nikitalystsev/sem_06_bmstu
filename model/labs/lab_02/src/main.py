from lsm_for_line import LeastSquaresMethodLine

import numpy as np
from matplotlib import pyplot as plt

from scipy.integrate import solve_ivp
from scipy.optimize import fsolve

# отладочные параметры
r = 0.35
t_w = 2000
t_0 = 1e4
p = 4

c = 3e10

# таблица значений k
t_k = [2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
k_1 = [8.2E-3, 2.768E-02, 6.560E-02, 1.281E-01, 2.214E-01, 3.516E-01, 5.248E-01, 7.472E-01, 1.025E+00]
k_2 = [1.600E+00, 5.400E+00, 1.280E+01, 2.500E+01, 4.320E+01, 6.860E+01, 1.024E+02, 1.458E+02, 2.000E+02]

# коэффициенты уравнений прямых при аппроксимации таблицы значений с
# коэффициентом поглощения
a1, b1 = LeastSquaresMethodLine(x=np.log(t_k), y=np.log(k_1)).get_solve()
a2, b2 = LeastSquaresMethodLine(x=np.log(t_k), y=np.log(k_2)).get_solve()

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
        return -3 * r * k1(z) / c * _f

    return -3 * r * k2(z) / c * _f


def der_f(z, u, _f):
    """
    Функция правой части первого уравнения
    f = f(z) - значение функции F в точке z
    u = u(z) - значение функции u в точке z
    """
    if is_k1:
        common_part = r * c * k1(z) * (u_p(z) - u)
    else:
        common_part = r * c * k2(z) * (u_p(z) - u)

    res = -_f / z + common_part if abs(z) > EPS else common_part / 2

    return res


def rk2(a, b, h, u_0, f_0):
    """
    Реализация метода Рунге Кутта 2-го порядка
    """

    alpha = 1  # задаваемый параметр
    half_h = h / 2

    z_res = np.arange(a, b + h, h)  # b не включительно, поэтому передаем чуть больше
    u_res = np.zeros(len(z_res))
    f_res = np.zeros(len(z_res))

    u_n = u_0
    f_n = f_0

    for i, z in enumerate(z_res):
        u_res[i] = u_n
        f_res[i] = f_n

        _k1 = der_u(z, f_n)
        _q1 = der_f(z, u_n, f_n)

        _k2 = der_u(z + half_h, f_n + half_h * _q1)
        _q2 = der_f(z + half_h, u_n + half_h * _k1, f_n + half_h * _q1)

        u_n += h * ((alpha - 1) * _k1 + alpha * _k2)
        f_n += h * ((alpha - 1) * _q1 + alpha * _q2)

    return z_res, u_res, f_res


def rk4(a, b, h, u_0, f_0):
    """
    Реализация метода Рунге Кутта 4-го порядка
    """
    half_h = h / 2

    z_res = np.arange(a, b + h, h)  # b не включительно, поэтому передаем чуть больше
    u_res = np.zeros(len(z_res))
    f_res = np.zeros(len(z_res))

    u_n = u_0
    f_n = f_0

    for i, z in enumerate(z_res):
        u_res[i] = u_n
        f_res[i] = f_n

        _k1 = der_u(z, f_n)
        _q1 = der_f(z, u_n, f_n)

        _k2 = der_u(z + half_h, f_n + half_h * _q1)
        _q2 = der_f(z + half_h, u_n + half_h * _k1, f_n + half_h * _q1)

        _k3 = der_u(z + half_h, f_n + half_h * _q2)
        _q3 = der_f(z + half_h, u_n + half_h * _k2, f_n + half_h * _q2)

        _k4 = der_u(z + h, f_n + h * _q3)
        _q4 = der_f(z + h, u_n + h * _k3, f_n + h * _q3)

        u_n += (h / 6) * (_k1 + 2 * _k2 + 2 * _k3 + _k4)
        f_n += (h / 6) * (_q1 + 2 * _q2 + 2 * _q3 + _q4)

    return z_res, u_res, f_res


def psi(u, f):
    """
    Функция правого краевого условия
    """

    return f - 0.393 * c * u


def get_init_cond(curr_ksi, a, b, h, method):
    """
    Метод для получения начальных условий при решении методом стрельбы
    """

    _, u, f = method(a, b, h, curr_ksi * u_p(0), 0)

    return psi(u[-1], f[-1])


def get_solve(a, b, h, method):
    """
    Метод, реализующий общее методов Рунге-Кутты
    """
    ksi_start, ksi_end = 1e-2, 1  # начальный интервал неопределенности
    ksi_curr = 0

    condition = True

    # реализация метода дихотомии для нахождения корня уравнения
    # psi(u(b, s), F(b, s)) = 0, где s - начальное значение в методе стрельбы
    while condition:
        ksi_curr = (ksi_start + ksi_end) / 2  # находим середину текущего интервала неопределенности

        f_ksi_start = get_init_cond(ksi_start, a, b, h, method)
        f_ksi_curr = get_init_cond(ksi_curr, a, b, h, method)
        f_ksi_end = get_init_cond(ksi_end, a, b, h, method)

        if f_ksi_start * f_ksi_curr < 0:
            ksi_end = ksi_curr
        if f_ksi_curr * f_ksi_end < 0:
            ksi_start = ksi_curr

        err = abs((ksi_end - ksi_start) / ksi_curr)

        if err <= EPS:
            condition = False

    u_0 = ksi_curr * u_p(0)

    z, u, f = method(a, b, h, u_0, 0)

    return z, u, f, ksi_start, ksi_end


def get_solve_by_auto_step(a, b, method):
    """
    Пытаюсь реализовать автоматический выбор шага
    """
    z = a
    h = 0.1

    z_res, u_res, f_res = list(), list(), list()

    cnt = 0

    while z <= b:
        # print(f"cacl by h")
        _, u_h, _, _, _ = get_solve(a, z + h, h, method)
        # print(f"cacl by h / 2")
        _, u_h_2, _, _, _ = get_solve(a, z + h, h / 2, method)

        # локальная погрешность по формуле Рунге
        abs_err = abs((u_h_2[-1] - u_h[-1]) / (1 - 1 / 2 ** 4))
        # print(f"abs_err = {abs_err: <10.7e}")

        cnt2 = 0
        while abs_err > EPS:
            h = h / 2

            _, u_h, _, _, _ = get_solve(a, z + h, h, method)
            _, u_h_2, _, _, _ = get_solve(a, z + h, h / 2, method)

            # локальная погрешность по формуле Рунге
            abs_err = abs((u_h_2[-1] - u_h[-1]) / (1 - 1 / 2 ** 4))

            cnt2 += 1

            if cnt2 % 10 == 0:
                print(f"Выполнено {cnt} итераций цикла уменьшения шага")

        _, u_h, f_h, _, _ = get_solve(a, z + h, h, method)

        cnt += 1

        if cnt % 10 == 0:
            print(f"Выполнено {cnt} итераций")

        z += h
        z_res.append(z)
        u_res.append(u_h[-1])
        f_res.append(f_h[-1])

        if abs_err < EPS / 32:
            h *= 2

        if z + h > b:
            break

    return z_res, u_res, f_res


def get_research():
    """
    Исследование правой прогонки по полной
    """
    table_size = 85
    a, b = 0, 1

    n_list = [100, 70, 50, 30, 20]

    file = open("../data/research.txt", "w", encoding="utf-8")

    file.write("-" * table_size + "\n")
    file.write(f' {"n": ^7} | {"u(0)": ^22} | {"u(1)": ^22} | {"f(1)": ^22} |\n')
    file.write("-" * table_size + "\n")

    for n in n_list:
        h = (b - a) / n

        z_res, u_res, f_res, ksi_start, ksi_end = get_solve(a, b, h, method=rk4)

        z_res = np.arange(a, b + h / 2, h)

        file.write(f"{n: 8} | {u_res[0]: ^22.6e} | {u_res[-1]: ^22.6e} | {f_res[-1]: ^22.6e} |\n")

    file.write("-" * table_size)

    file.close()


def write_result_to_file(filepath, z_res, u_res, f_res):
    """
    Запись результатов в файл
    """
    file = open(filepath, "w", encoding="utf-8")

    file.write(f"Число узлов n = {len(z_res)}\n")
    file.write("-" * 61 + "\n")
    file.write(f'| {"x": ^7} | {"u(z)": ^22} | {"f(z)": ^22} |\n')
    file.write("-" * 61 + "\n")

    # for i in range(len(z_res)):
    #     file.write(f"| {z_res[i]: ^7.5f} | {u_res[i]: ^22.6e} | {f_res[i]: ^22.6e} |\n")

    for i in [0, len(u_res) - 1]:
        file.write(f"| {z_res[i]: ^7.5f} | {u_res[i]: ^22.6e} | {f_res[i]: ^22.6e} |\n")

    file.write("-" * 61)

    file.close()


def main() -> None:
    """
    Главная функция
    """
    get_research()
    # a, b = 0, 1
    # n = 200  # число узлов
    # h = (b - a) / n
    #
    # # # z_res, u_res, f_res, ksi_start, ksi_end = get_solve_by_rk(a, b, h, method=rk2)
    # z_res, u_res, f_res, ksi_start, ksi_end = get_solve(a, b, h, method=rk4)
    # # # z_res, u_res, f_res = get_solve_by_auto_step(a, b, method=rk2)
    # # z_res, u_res, f_res = get_solve_by_auto_step(a, b, method=rk4)
    # #
    # up_res = [0] * len(z_res)
    #
    # for i in range(len(z_res)):
    #     up_res[i] = u_p(z_res[i])
    # #
    # # # write_result_to_file("../data/rk2.txt", z_res, u_res, f_res)
    # write_result_to_file("../data/rk4.txt", z_res, u_res, f_res)
    # # write_result_to_file("../data/auto_step.txt", z_res, u_res, f_res)
    #
    # plt.figure(figsize=(9, 6))
    # plt.subplot(2, 2, 1)
    # plt.plot(z_res, u_res, 'r', label='u(z)')
    # plt.plot(z_res, up_res, 'b', label='u_p')
    # plt.legend()
    # plt.grid()
    #
    # plt.subplot(2, 2, 2)
    # plt.plot(z_res, f_res, 'g', label='F(z)')
    # plt.legend()
    # plt.grid()
    #
    # plt.subplot(2, 2, 3)
    # plt.plot(z_res, f_res2, 'g', label='F(z) integral')
    # plt.legend()
    # plt.grid()
    #
    # plt.subplot(2, 2, 4)
    # plt.plot(z_res, div_f, 'y', label='divF(z)')
    # plt.legend()
    # plt.grid()
    #
    plt.show()

    # cmp_res_by_input_data(a, b, h)


if __name__ == '__main__':
    main()
