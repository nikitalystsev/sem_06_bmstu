import numpy as np
from dataclasses import dataclass
from matplotlib import pyplot as plt


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
    f0: int | float = 1
    beta: int | float = 1
    # координаты x0, z0 центра распределения функции f(x,z) задаются пользователем.
    x0: int | float = 7
    z0: int | float = 7


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


def _lambda():
    """
    Функция λ(x, z) = λ
    """

    return 0.1


def f(x, z, ops: TaskOps):
    """
    Функция f(x, z)
    """
    f0, beta, x0, z0 = ops.f0, ops.beta, ops.x0, ops.z0

    return f0 * np.exp(-beta * ((x - x0) ** 2 + (z - z0) ** 2))


def left_bc(ops: TaskOps):
    """
    Левое краевое условие прогонки (все КУ - 1-го рода)
    """
    u0 = ops.u0

    m_0 = 0
    k_0 = 1
    p_0 = u0

    return k_0, m_0, p_0


def right_bc(ops: TaskOps):
    """
    Правое краевое условие прогонки (все КУ - 1-го рода)
    """
    u0 = ops.u0

    k_n = 0
    m_n = 1
    p_n = u0

    return k_n, m_n, p_n


def right_sweep_by_x(prev_mtr_u, k, grid: Grid, ops: TaskOps):
    """
    Реализация правой прогонки по координате x для локально одномерного метода
    """
    a, b, h_x, h_z, tau = grid.a, grid.b, grid.h_x, grid.h_z, grid.tau

    # Прямой ход
    k_0, m_0, p_0 = left_bc(ops)
    k_n, m_n, p_n = right_bc(ops)

    ksi = [0, -m_0 / k_0]
    eta = [0, p_0 / k_0]

    z_list = np.arange(0, b + h_z, h_z)
    x = h_x
    n = 1

    # фиксируем индексом k строку матрицы
    for i in range(len(prev_mtr_u[0])):
        a_n = 1 / (h_x ** 2)
        d_n = 1 / (h_x ** 2)
        b_n = 2 * a_n + 1 / tau
        f_n = (prev_mtr_u[k][i] / tau + f(x, z_list[k], ops) / (2 * _lambda()))

        ksi.append(d_n / (b_n - a_n * ksi[n]))
        eta.append((a_n * eta[n] + f_n) / (b_n - a_n * ksi[n]))

    n += 1
    x += h_x

    # Обратный ход
    u = [0] * len(prev_mtr_u[0])

    u[-1] = (p_n - k_n * eta[-1]) / (k_n * ksi[-1] + m_n)

    for i in range(len(u) - 2, -1, -1):
        u[i] = ksi[i + 1] * u[i + 1] + eta[i + 1]

    return u


def right_sweep_by_z(prev_mtr_u, n, grid: Grid, ops: TaskOps):
    """
    Реализация правой прогонки для локально одномерного метода
    """
    a, b, h_x, h_z, tau = grid.a, grid.b, grid.h_x, grid.h_z, grid.tau

    # Прямой ход
    k_0, m_0, p_0 = left_bc(ops)
    k_n, m_n, p_n = right_bc(ops)

    ksi = [0, -m_0 / k_0]
    eta = [0, p_0 / k_0]

    x_list = np.arange(0, a + h_x, h_x)
    z = h_z
    _n = 1

    for i in range(len(prev_mtr_u)):
        a_n = 1 / (h_z ** 2)
        d_n = 1 / (h_z ** 2)
        b_n = 2 * a_n + 1 / tau
        f_n = (prev_mtr_u[i][n] / tau + f(x_list[n], z, ops) / (2 * _lambda()))

        ksi.append(d_n / (b_n - a_n * ksi[_n]))
        eta.append((a_n * eta[_n] + f_n) / (b_n - a_n * ksi[_n]))

        _n += 1
        z += h_z

    # Обратный ход
    u = [0] * len(prev_mtr_u)

    u[-1] = (p_n - k_n * eta[-1]) / (k_n * ksi[-1] + m_n)

    for i in range(len(u) - 2, -1, -1):
        u[i] = ksi[i + 1] * u[i + 1] + eta[i + 1]

    return u


def is_small_diff(prev_layer, cur_layer):
    """
    Введя фиктивное время, нужно наблюдать, когда при очередном поиске решения
    значения функции на текущем слое будут отличаться от решения, полученного
    на предыдущем слое, на заданное eps
    """
    eps = 1e-3

    for i in range(len(prev_layer)):
        for j in range(len(prev_layer[0])):
            if abs((cur_layer[i][j] - prev_layer[i][j]) / prev_layer[i][j]) >= eps:
                return False

    return True


def solve(prev_mtr_u: list[list[int | float]], grid: Grid, ops: TaskOps):
    """
    Функция поиска текущего решения (реализация локально одномерного метода)
    """
    k, n = grid.k, grid.n
    u0 = ops.u0

    tmp_mtr_u = []  # значения на промежуточном слое

    # прогонка для каждого k
    for i in range(1, k):
        tmp_u = right_sweep_by_x(prev_mtr_u, i, grid, ops)
        tmp_mtr_u.append(tmp_u)

    tmp_mtr_u.insert(0, [u0 for _ in range(n + 1)])
    tmp_mtr_u.append([u0 for _ in range(n + 1)])

    curr_mtr_u = []  # значения на новом слое

    # прогонка для каждого n
    for i in range(1, n):
        curr_u = right_sweep_by_z(tmp_mtr_u, i, grid, ops)
        curr_mtr_u.append(curr_u)

    curr_mtr_u.insert(0, [u0 for _ in range(k + 1)])
    curr_mtr_u.append([u0 for _ in range(k + 1)])

    np_matrix = np.array(curr_mtr_u)
    transposed = list(np_matrix.T)

    return transposed


def get_solve(grid: Grid, ops: TaskOps):
    """
    Функция получения ВСЕГО решения
    """
    u0 = ops.u0

    n, k = grid.n, grid.k
    # хз почему в начальный фиктивный момент времени вся матрица u0
    prev_mtr_u = [[u0 for _ in range(n + 1)] for _ in range(k + 1)]  # предыдущий слой (на котором все известно)

    curr_mtr_u = solve(prev_mtr_u, grid, ops)  # значения, полученные на текущем слое

    c = 0

    while not is_small_diff(prev_mtr_u, curr_mtr_u):
        prev_mtr_u = curr_mtr_u
        curr_mtr_u = solve(prev_mtr_u, grid, ops)

        print(f"ИТЕРАЦИЯ НОМЕР {c + 1}")
        c += 1

    return curr_mtr_u


def main() -> None:
    """
    Главная функция
    """
    ops = TaskOps()
    n = 1000  # число узлов по x (на деле узлов n + 1)
    h_x = ops.a / n  # шаг по координате
    k = 1000  # число узлов по z (на деле узлов k + 1)
    h_z = ops.b / k

    grid = Grid(ops.a, n, h_x, ops.b, k, h_z, tau=1)

    u_res = get_solve(grid, ops)

    x = np.linspace(0, ops.a, len(u_res[0]))
    z = np.linspace(0, ops.b, len(u_res))

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
