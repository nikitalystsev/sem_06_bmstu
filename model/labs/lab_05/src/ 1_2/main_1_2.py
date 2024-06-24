"""
Жалка попытка сделать самое сложное
Уравнение -- 1-й вариант
Краевые условия -- 2-й вариант
Экономичная схема: продольно-поперечный метод
"""
# ЭТО НЕРАБОТАЮЩАЯ ХУЙНЯ !!!!!!!!!!!!!!!!!!!!!

import numpy as np
from dataclasses import dataclass
from matplotlib import pyplot as plt

EPS = 1e-5


class TaskOps:
    """
    Класс параметров задачи
    """
    a1: int | float = 0.0134
    b1: int | float = 1
    c1: int | float = 4.35e-4
    m1: int | float = 1
    # параметры alphai:
    alpha1: int | float = 0.05
    alpha2: int | float = 0.05
    alpha3: int | float = 0.05
    alpha4: int | float = 0.05
    # для отладки геометрические параметры прямоугольника
    a: int | float = 10
    b: int | float = 10

    u0: int | float = 300
    flux0: int | float = 30  # flux - поток при x = 0
    # f0, beta варьируются исходя из условия, чтобы максимум решения
    # уравнения - функции u (x,z) не превышал 3000К
    f0: int | float = 30
    beta: int | float = 1
    # координаты x0, z0 центра распределения функции f(x,z) задаются пользователем.
    x0: int | float = 5
    z0: int | float = 5


@dataclass
class Grid:
    """
    Класс -- хранитель числа узлов, шагов по каждой переменной
    (сетка, крч)
    """
    a: int | float  # по x координате ОС от 0
    n: int
    h_x: int | float

    b: int | float  # по z координате ОА от 0
    k: int
    h_z: int | float

    tau: int | float  # шаг по фиктивному времени


def _lambda(u, ops: TaskOps):
    """
    Функция λ(u)
    """
    a1, b1, c1, m1 = ops.a1, ops.b1, ops.c1, ops.m1

    return a1 * (b1 + c1 * u ** m1)


def kappa(u1, u2, ops: TaskOps):
    """
    Каппа
    """

    return (_lambda(u1, ops) + _lambda(u2, ops)) / 2


def f(x, z, ops: TaskOps):
    """
    Функция f(x, z)
    """
    f0, beta, x0, z0 = ops.f0, ops.beta, ops.x0, ops.z0

    return f0 * np.exp(-beta * ((x - x0) ** 2 + (z - z0) ** 2))


def left_bound_cond_by_x(k, z_k, prev_mtr_u, curr_mtr_u, grid: Grid, ops: TaskOps):
    """
    Левое краевое условие прогонки (x = 0)
    """
    h_x, h_z, tau = grid.h_x, grid.h_z, grid.tau
    u0, alpha1 = ops.alpha1, ops.u0

    y0, y1 = curr_mtr_u[k][0], curr_mtr_u[k][1]
    prev_y0, prev_y1 = prev_mtr_u[k][0], prev_mtr_u[k][1]

    f_half = (f(0, z_k, ops) + f(0 + h_x, z_k, ops)) / 2

    k_0_x = 3 * h_x * h_z / 8 + alpha1 * h_z * tau / 2 + kappa(y0, y1, ops) * h_z * tau / (2 * h_x)

    m_0_x = h_x * h_z / 8 - kappa(y0, y1, ops) * h_z * tau / (2 * h_x)

    # ну ок, предположим что с краю потока G нет
    p_0_x = (f(0, z_k, ops) + f_half) * h_x * h_z * tau / 4 + h_x * h_z * (
            prev_y0 + prev_y1) / 8 + prev_y0 * h_x * h_z / 4 + alpha1 * u0 * h_z * tau / 2

    return k_0_x, m_0_x, p_0_x


def right_bound_cond_by_x(k, z_k, prev_mtr_u, curr_mtr_u, grid: Grid, ops: TaskOps):
    """
    Правое краевое условие прогонки (x = a)
    """
    h_x, h_z, tau = grid.h_x, grid.h_z, grid.tau
    a, u0, alpha2 = ops.a, ops.u0, ops.alpha2

    yn, yn_1 = curr_mtr_u[k][-1], curr_mtr_u[k][-2]
    prev_yn, prev_yn_1 = prev_mtr_u[k][-1], prev_mtr_u[k][-2]

    f_half = (f(a, z_k, ops) + f(a - h_x, z_k, ops)) / 2

    k_n_x = h_x * h_z / 8 - kappa(yn, yn_1, ops) * h_z * tau / (2 * h_x)

    m_n_x = 3 * h_x * h_z / 8 + alpha2 * h_z * tau / 2 + kappa(yn, yn_1, ops) * h_z * tau / (2 * h_x)

    # ну ок, предположим что с краю потока G нет
    p_n_x = (f_half + f(a, z_k, ops)) * h_x * h_z * tau / 4 + h_x * h_z * (
            prev_yn + prev_yn_1) / 8 + prev_yn * h_x * h_z / 4 + alpha2 * u0 * h_z * tau / 2

    return k_n_x, m_n_x, p_n_x


def left_bound_cond_by_z(n, x_n, prev_mtr_u, curr_mtr_u, grid: Grid, ops: TaskOps):
    """
    Левое краевое условие прогонки (z = 0)
    """
    h_x, h_z, tau = grid.h_x, grid.h_z, grid.tau
    u0, alpha3 = ops.alpha3, ops.u0

    y0, y1 = curr_mtr_u[0][n], curr_mtr_u[1][n]
    prev_y0, prev_y1 = prev_mtr_u[0][n], prev_mtr_u[1][n]

    f_half = (f(x_n, 0, ops) + f(x_n, 0 + h_z, ops)) / 2

    k_0_z = 3 * h_x * h_z / 8 + alpha3 * h_z * tau / 2 + kappa(y0, y1, ops) * h_z * tau / (2 * h_x)

    m_0_z = h_x * h_z / 8 - kappa(y0, y1, ops) * h_z * tau / (2 * h_x)

    # ну ок, предположим что с краю потока F нет
    p_0_z = (f(x_n, 0, ops) + f_half) * h_x * h_z * tau / 4 + h_x * h_z * (
            prev_y0 + prev_y1) / 8 + prev_y0 * h_x * h_z / 4 + alpha3 * u0 * h_z * tau / 2

    return k_0_z, m_0_z, p_0_z


def right_bound_cond_by_z(n, x_n, prev_mtr_u, curr_mtr_u, grid: Grid, ops: TaskOps):
    """
    Правое краевое условие прогонки (z = b)
    """
    h_x, h_z, tau = grid.h_x, grid.h_z, grid.tau
    b, u0, alpha4 = ops.b, ops.u0, ops.alpha4

    yn, yn_1 = curr_mtr_u[-1][n], curr_mtr_u[-2][n]
    prev_yn, prev_yn_1 = prev_mtr_u[-1][n], prev_mtr_u[-2][n]

    f_half = (f(x_n, b, ops) + f(x_n, b - h_z, ops)) / 2

    k_n_z = h_x * h_z / 8 - kappa(yn, yn_1, ops) * h_z * tau / (2 * h_x)

    m_n_z = 3 * h_x * h_z / 8 + alpha4 * h_z * tau / 2 + kappa(yn, yn_1, ops) * h_z * tau / (2 * h_x)

    # ну ок, предположим что с краю потока F нет
    p_n_z = (f_half + f(x_n, b, ops)) * h_x * h_z * tau / 4 + h_x * h_z * (
            prev_yn + prev_yn_1) / 8 + prev_yn * h_x * h_z / 4 + alpha4 * u0 * h_z * tau / 2

    return k_n_z, m_n_z, p_n_z


def right_sweep_by_x(k, prev_mtr_u, curr_mtr_u, grid: Grid, ops: TaskOps):
    """
    Реализация правой прогонки по координате x
    """
    b = ops.b
    h_z, h_x, tau = grid.h_z, grid.h_x, grid.tau

    z_list = np.arange(0, b + h_z, h_z)

    k0, m0, p0 = left_bound_cond_by_x(k, z_list[k], prev_mtr_u, curr_mtr_u, grid, ops)
    kn, mn, pn = right_bound_cond_by_x(k, z_list[k], prev_mtr_u, curr_mtr_u, grid, ops)

    ksi = [0, -m0 / k0]
    eta = [0, p0 / k0]

    x = h_x
    n = 1

    # фиксируем индексом k строку матрицы
    for i in range(1, len(prev_mtr_u[0]) - 1):
        a_n = kappa(curr_mtr_u[k][i - 1], curr_mtr_u[k][i], ops) * h_z * tau / (2 * h_x)
        c_n = kappa(curr_mtr_u[k][i], curr_mtr_u[k][i + 1], ops) * h_z * tau / (2 * h_x)
        b_n = a_n + c_n + h_x * h_z

        if k == 0:  # я пока не понял как это правильно обрабатывать
            f_n = prev_mtr_u[k][i] * h_x * h_z + (kappa(prev_mtr_u[k][i], prev_mtr_u[k][i + 1], ops)
                                                  * (prev_mtr_u[k][i] - prev_mtr_u[k + 1][i]) / h_z
                                                  ) * tau * h_x / 2 + f(x, z_list[k], ops) * h_x * h_z * tau / 2
        if k == len(prev_mtr_u) - 1:
            f_n = prev_mtr_u[k][i] * h_x * h_z + (kappa(prev_mtr_u[k][i - 1], prev_mtr_u[k][i], ops)
                                                  * (prev_mtr_u[k - 1][i] - prev_mtr_u[k][i]) / h_z
                                                  ) * tau * h_x / 2 + f(x, z_list[k], ops) * h_x * h_z * tau / 2
        else:
            f_n = prev_mtr_u[k][i] * h_x * h_z + (kappa(prev_mtr_u[k][i - 1], prev_mtr_u[k][n], ops)
                                                  * (prev_mtr_u[k - 1][i] - prev_mtr_u[k][i]) / h_z -
                                                  kappa(prev_mtr_u[k][i], prev_mtr_u[k][n + 1], ops)
                                                  * (prev_mtr_u[k][i] - prev_mtr_u[k + 1][i]) / h_z
                                                  ) * tau * h_x / 2 + f(x, z_list[k], ops) * h_x * h_z * tau / 2

        ksi.append(c_n / (b_n - a_n * ksi[n]))
        eta.append((a_n * eta[n] + f_n) / (b_n - a_n * ksi[n]))

        n += 1
        x += h_x

    # Обратный ход
    u = [0] * len(prev_mtr_u[0])

    u[-1] = (pn - kn * eta[-1]) / (kn * ksi[-1] + mn)

    for i in range(len(u) - 2, -1, -1):
        u[i] = ksi[i + 1] * u[i + 1] + eta[i + 1]

    return u


def right_sweep_by_z(n, prev_mtr_u, curr_mtr_u, grid: Grid, ops: TaskOps):
    """
    Реализация правой прогонки по координате x
    """
    a = ops.a
    h_z, h_x, tau = grid.h_z, grid.h_x, grid.tau

    x_list = np.arange(0, a + h_x, h_x)

    k0, m0, p0 = left_bound_cond_by_z(n, x_list[n], prev_mtr_u, curr_mtr_u, grid, ops)
    kn, mn, pn = right_bound_cond_by_z(n, x_list[n], prev_mtr_u, curr_mtr_u, grid, ops)

    ksi = [0, -m0 / k0]
    eta = [0, p0 / k0]

    z = h_z
    _n = 1

    # фиксируем индексом n столбец матрицы
    for i in range(1, len(prev_mtr_u) - 1):
        a_n = kappa(curr_mtr_u[i - 1][n], curr_mtr_u[i][n], ops) * h_x * tau / (2 * h_z)
        c_n = kappa(curr_mtr_u[i][n], curr_mtr_u[i + 1][n], ops) * h_x * tau / (2 * h_z)
        b_n = a_n + c_n + h_x * h_z

        if n == 0:  # я пока не понял как это правильно обрабатывать
            f_n = prev_mtr_u[i][n] * h_x * h_z + (kappa(prev_mtr_u[i][n], prev_mtr_u[i][n + 1], ops)
                                                  * (prev_mtr_u[i][n] - prev_mtr_u[i][n + 1]) / h_x
                                                  ) * tau * h_x / 2 + f(x_list[n], z, ops) * h_x * h_z * tau / 2
        if n == len(prev_mtr_u[0]) - 1:
            f_n = prev_mtr_u[i][n] * h_x * h_z + (kappa(prev_mtr_u[i][n - 1], prev_mtr_u[i][n], ops)
                                                  * (prev_mtr_u[i][n - 1] - prev_mtr_u[i][n]) / h_x
                                                  ) * tau * h_x / 2 + f(x_list[n], z, ops) * h_x * h_z * tau / 2
        else:
            f_n = prev_mtr_u[i][n] * h_x * h_z + (kappa(prev_mtr_u[i][n - 1], prev_mtr_u[i][n], ops)
                                                  * (prev_mtr_u[i][n - 1] - prev_mtr_u[i][n]) / h_x -
                                                  kappa(prev_mtr_u[i][n], prev_mtr_u[i][n + 1], ops)
                                                  * (prev_mtr_u[i][n] - prev_mtr_u[i][n + 1]) / h_x
                                                  ) * tau * h_z / 2 + f(x_list[n], z, ops) * h_x * h_z * tau / 2

        ksi.append(c_n / (b_n - a_n * ksi[_n]))
        eta.append((a_n * eta[_n] + f_n) / (b_n - a_n * ksi[_n]))

        _n += 1
        z += h_z

    # Обратный ход
    u = [0] * len(prev_mtr_u)

    u[-1] = (pn - kn * eta[-1]) / (kn * ksi[-1] + mn)

    for i in range(len(u) - 2, -1, -1):
        u[i] = ksi[i + 1] * u[i + 1] + eta[i + 1]

    return u


def simple_iterations_by_x_layer(k, prev_mtr_u, curr_mtr_u, grid: Grid, ops: TaskOps):
    """
    Метод простых итераций для прогонки по координате x
    """
    _curr_mtr_u = curr_mtr_u  # значения температуры на текущем слое

    c = 0

    while True:
        # цикл подсчета значений функции u методом простых итераций для
        # след фиктивного временного слоя
        curr_u = right_sweep_by_x(k, prev_mtr_u, _curr_mtr_u, grid, ops)

        cnt = 0

        for i in range(len(curr_u)):
            curr_err = abs((_curr_mtr_u[k][i] - curr_u[i]) / curr_u[i])
            if curr_err < EPS:
                cnt += 1

        if cnt == len(curr_u):
            break

        _curr_mtr_u[k] = curr_u

        # print(f"итерация по x №{c + 1}")
        c += 1

    return _curr_mtr_u[k]


def simple_iterations_by_z_layer(n, prev_mtr_u, curr_mtr_u, grid: Grid, ops: TaskOps):
    """
    Метод простых итераций для прогонки по координате z
    """
    _curr_mtr_u = curr_mtr_u  # значения температуры на текущем слое

    while True:
        # цикл подсчета значений функции u методом простых итераций для
        # след фиктивного временного слоя
        curr_u = right_sweep_by_z(n, prev_mtr_u, _curr_mtr_u, grid, ops)

        cnt = 0

        for i in range(len(curr_u)):
            curr_err = abs((_curr_mtr_u[i][n] - curr_u[i]) / curr_u[i])
            if curr_err < EPS:
                cnt += 1

        if cnt == len(curr_u):
            break

        for i in range(len(_curr_mtr_u)):
            _curr_mtr_u[i][n] = curr_u[i]

    return [_curr_mtr_u[i][n] for i in range(len(_curr_mtr_u))]


def is_small_diff(prev_layer, curr_layer):
    """
    Введя фиктивное время, нужно наблюдать, когда при очередном поиске решения
    значения функции на текущем слое будут отличаться от решения, полученного
    на предыдущем слое, на заданное eps
    """
    eps = 1e-3

    for i in range(len(prev_layer)):
        for j in range(len(prev_layer[0])):
            err = abs((curr_layer[i][j] - prev_layer[i][j]) / prev_layer[i][j])
            if err >= eps:
                print(f"err = {err}")
                return False

            print(f"err = {err}")
    return True


def get_solve(grid: Grid, ops: TaskOps):
    """
    Функция получения ВСЕГО решения
    """
    n, k = grid.n, grid.k
    u0 = ops.u0

    x_list = np.linspace(0, ops.a, n + 1)
    z_list = np.linspace(0, ops.b, k + 1)

    # значения с предыдущего слоя (на котором все известно)
    prev_mtr_u = [[u0 for _ in range(n + 1)] for _ in range(k + 1)]
    # значения с текущего слоя (на котором все известно)
    curr_mtr_u = [[u0 for _ in range(n + 1)] for _ in range(k + 1)]
    c = 0

    while True:
        tmp_mtr_u = []  # значения на промежуточном слое

        # прогонка для каждого k
        for i in range(k + 1):
            tmp_u = simple_iterations_by_x_layer(i, prev_mtr_u, curr_mtr_u, grid, ops)
            tmp_mtr_u.append(tmp_u)

        new_mtr_u = []  # значения на новом слое

        # прогонка для каждого n
        for i in range(n + 1):
            curr_u = simple_iterations_by_z_layer(i, prev_mtr_u, tmp_mtr_u, grid, ops)
            new_mtr_u.append(curr_u)

        curr_mtr_u = np.array(new_mtr_u)
        curr_mtr_u = list(curr_mtr_u.T)

        if is_small_diff(prev_mtr_u, curr_mtr_u):
            break

        prev_mtr_u = curr_mtr_u

        print(f"ИТЕРАЦИЯ НОМЕР {c + 1}")
        c += 1

    return x_list, z_list, curr_mtr_u


def main() -> None:
    """
    Главная функция
    """
    ops = TaskOps()
    n = 50  # число узлов по x (на деле узлов n + 1)
    h_x = ops.a / n  # шаг по координате
    k = 50  # число узлов по z (на деле узлов k + 1)
    h_z = ops.b / k

    print(f"h_x = {h_x}, h_z = {h_z}")

    grid = Grid(ops.a, n, h_x, ops.b, k, h_z, tau=2)

    x, z, u_res = get_solve(grid, ops)

    X, Y = np.meshgrid(x, z)

    farr = np.array([np.array(T_m) for T_m in u_res])
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X, Y, farr, cmap="viridis")

    ax.set_xlabel("x")
    ax.set_ylabel("z")
    ax.set_zlabel("U(x, z)")
    plt.show()

    plt.imshow(u_res, cmap='viridis')
    plt.colorbar()
    plt.show()


if __name__ == '__main__':
    main()
