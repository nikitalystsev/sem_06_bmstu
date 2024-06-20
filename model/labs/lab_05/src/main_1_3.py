import numpy as np
from dataclasses import dataclass


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
    f0: int | float
    beta: int | float
    # координаты x0, z0 центра распределения функции f(x,z) задаются пользователем.
    x0: int | float
    z0: int | float


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


def _lambda(u, ops: TaskOps):
    """
    Функция λ(u)
    """
    a1, b1, c1, m1 = ops.a1, ops.b1, ops.c1, ops.m1

    return a1 * (b1 + c1 * u ** m1)


def f(x, z, ops: TaskOps):
    """
    Функция f(x, z)
    """
    f0, beta, x0, z0 = ops.f0, ops.beta, ops.x0, ops.z0

    return f0 * np.exp(-beta * ((x - x0) ** 2 + (z - z0) ** 2))


def is_small_diff(prev_mtr_u, curr_mtr_u):
    """
    Введя фиктивное время, нужно наблюдать, когда при очередном поиске решения
    значения функции на текущем слое будут отличаться от решения, полученного
    на предыдущем слое, на заданное eps
    """
    eps = 1e-3
    n, k = len(prev_mtr_u), len(prev_mtr_u[0])

    for i in range(n):
        for j in range(k):
            err = abs((curr_mtr_u[i][j] - prev_mtr_u[i][j]) / prev_mtr_u[i][j])
            if err > eps:
                return False

    return True


def get_solve(grid: Grid, ops: TaskOps):
    """
    Функция получения решения
    """
    n, k = grid.n, grid.k
    u0 = ops.u0

    curr_mtr = np.full((n + 1, k + 1), u0)  # текущий слой (ищется)
    prev_mtr = np.full((n + 1, k + 1), u0 - 1)  # предыдущ слой (на нем все известно)
    tmp_mtr = np.full((n + 1, k + 1), u0)  # промежуточный слой (tau / 2)

    while not is_small_diff(prev_mtr, curr_mtr):
        for i in range(n + 1):
            for j in range(k + 1):
                prev_mtr[i][j] = curr_mtr[i][j]
        # ++ прогонка для m от 1 до M - 1
        for j in range(1, k):
            # ++ метод простой итерации
            current_vector = [0] * (n + 1)
            for i in range(n + 1):
                current_vector[i] = prev_mtr[i][k]
            while True:
                # ++ прогонка для определённого m
                A_line = get_A_line(h_x, h_z, last_matrix, m, current_vector)
                B_line = get_B_line(h_x, h_z, last_matrix, m, current_vector)
                C_line = get_C_line(h_x, h_z, last_matrix, m, current_vector)
                D_line = get_D_line(h_x, h_z, last_matrix, m, current_vector)
                tmp_vector = calc_slae(A_line, B_line, C_line, D_line)
                # -- прогонка для определённого m

                # ++ выход из простой итерации
                if check_vector(current_vector, tmp_vector):
                    break
                # -- выход из простой итерации

                # ++ новое стартовое значение для простой итерации
                for n in range(N + 1):
                    current_vector[n] = (tmp_vector[n] + current_vector[n]) / 2
                # -- новое стартовое значение для простой итерации
            for n in range(N + 1):
                tmp_matrix[n][m] = current_vector[n]
            # -- метод простой итерации
        # -- прогонка для m от 1 до M - 1

def main() -> None:
    """
    Главная функция
    """
    ops = TaskOps()
    n = 100  # число узлов по x (на деле узлов n + 1)
    h_x = ops.a / n  # шаг по координате
    k = 100  # число узлов по z (на деле узлов k + 1)
    h_z = ops.b / k

    grid = Grid(ops.a, n, h_x, ops.b, k, h_z)


if __name__ == '__main__':
    main()
