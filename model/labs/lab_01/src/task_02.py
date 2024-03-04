import math as m
import matplotlib.pyplot as plt
import numpy as np


# 1 - 2 * x * u * u' = u ^ 3 * u'
# u(0.5) = 0

def get_x_u_by_analyt(u: int | float | np.ndarray) -> int | float | np.ndarray:
    """
    Функция аналитического решения
    """

    return np.exp(u ** 2) - (u ** 2) / 2 - 1 / 2


def get_x_u_by_picard1(u: int | float | np.ndarray) -> int | float | np.ndarray:
    """
    Функция решения методом Пикара (1-е приближение)
    """

    return 0.5 + (u ** 2) / 2 + (u ** 4) / 4


def get_x_u_by_picard2(u: int | float | np.ndarray) -> int | float | np.ndarray:
    """
    Функция решения методом Пикара (2-е приближение)
    """

    return 0.5 + (u ** 16) / 12 + (u ** 4) / 2 + (u ** 2) / 2


def get_x_u_by_picard3(u: int | float | np.ndarray) -> int | float | np.ndarray:
    """
    Функция решения методом Пикара (3-е приближение)
    """

    return 0.5 + (u ** 18) / 108 + (u ** 6) / 6 + (u ** 4) / 2 + (u ** 2) / 2


def get_x_u_by_picard4(u: int | float | np.ndarray) -> int | float | np.ndarray:
    """
    Функция решения методом Пикара (4-е приближение)
    """

    return 0.5 + (u ** 20) / 1080 + (u ** 8) / 24 + (u ** 6) / 6 + (u ** 4) / 2 + (u ** 2) / 2


def get_x_u_by_picard5(u: int | float | np.ndarray) -> int | float | np.ndarray:
    """
    Функция решения методом Пикара (4-е приближение)
    """

    return 0.5 + (u ** 22) / 1080 + (u ** 10) / 24 + (u ** 8) / 6 + (u ** 6) / 2 + 3 * (u ** 4) / 4 + (u ** 2) / 2


def get_solution() -> None:
    """
    Функция выводит все решения задачи
    """

    # try:
    #     arg = float(input("Введите значение аргумента: "))
    # except ValueError:
    #     print("Неверный ввод!")
    #     return

    # print(f"Аналитическое решение:                    x({arg}) = ", get_x_u_by_analyt(arg))
    # print(f"Решение методом Пикара (1-е приближение): x({arg}) = ", get_x_u_by_picard1(arg))
    # print(f"Решение методом Пикара (2-е приближение): x({arg}) = ", get_x_u_by_picard2(arg))
    # print(f"Решение методом Пикара (3-е приближение): x({arg}) = ", get_x_u_by_picard3(arg))
    # print(f"Решение методом Пикара (4-е приближение): x({arg}) = ", get_x_u_by_picard4(arg))
    # print(f"Решение методом Пикара (5-е приближение): x({arg}) = ", get_x_u_by_picard5(arg))

    fig1 = plt.figure(figsize=(10, 7))
    plot = fig1.add_subplot()

    u_values: np.ndarray | tuple[np.ndarray, float | None] = np.arange(0, 6, 0.001)

    plot.plot(get_x_u_by_analyt(u_values), u_values, label="Аналитическое решение")
    plot.plot(get_x_u_by_picard1(u_values), u_values, label="Метод Пикара (1-е приближение)")
    plot.plot(get_x_u_by_picard2(u_values), u_values, label="Метод Пикара (2-е приближение)")
    plot.plot(get_x_u_by_picard3(u_values), u_values, label="Метод Пикара (3-е приближение)")
    plot.plot(get_x_u_by_picard4(u_values), u_values, label="Метод Пикара (4-е приближение)")

    plt.legend()
    plt.grid()
    plt.title("Сравнение методов")

    plt.show()
