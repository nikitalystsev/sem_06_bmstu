import numpy as np


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


def main() -> None:
    """
    Главная функция
    """


if __name__ == '__main__':
    main()
