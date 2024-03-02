import matplotlib.pyplot as plt
from typing import Callable

MAX_X = 2.003
STEP = 1e-4


# u'(x) = x^2 + u^2
# u(0) = 0

def f(x: int | float, u: int | float) -> int | float:
    return x ** 2 + u ** 2


def get_u_x_by_picard1(x: int | float) -> int | float:
    """
    Функция решения методом Пикара (1-е приближение)
    """

    return x ** 3 / 3


def get_u_x_by_picard2(x: int | float) -> int | float:
    """
    Функция решения методом Пикара (2-е приближение)
    """

    return get_u_x_by_picard1(x) + x ** 7 / 63


def get_u_x_by_picard3(x: int | float) -> int | float:
    """
    Функция решения методом Пикара (3-е приближение)
    """

    return get_u_x_by_picard2(x) + x ** 15 / 59535 + (2 * x ** 11) / 2079


def get_u_x_by_picard4(x: int | float) -> int | float:
    """
    Функция решения методом Пикара (4-е приближение)
    """

    return get_u_x_by_picard2(x) + \
        (2 * x ** 11) / 2079 + \
        (13 * x ** 15) / 218295 + \
        (82 * x ** 19) / 37328445 + \
        (662 * x ** 23) / 10438212015 + \
        (4 * x ** 27) / 3341878155 + \
        (x ** 31) / 109876903975


def get_picard_approx(x_max, h, u_x_by_picard_func: Callable[[int | float], int | float]) -> list[int | float]:
    """
    Функция для получения массива значений функции методом Пикара переданного приближения
    """
    u_values = []
    x, u = 0, 0

    while abs(x) < abs(x_max):
        u_values.append(u)
        x += h
        u = u_x_by_picard_func(x)

    return u_values


def get_euler_approx(x_max, h) -> list[int | float]:
    """
    Функция для получения массива значений функции методом Эйлера
    """
    u_values = []
    x, u = 0, 0

    while abs(x) < abs(x_max):
        u_values.append(u)
        u = u + h * f(x, u)
        x += h

    return u_values


def get_generate_x(x_max, step) -> list[int | float]:
    """
    Функция для генерации диапазона значений аргумента с заданным шагом
    """
    x_values = []

    x = 0

    while abs(x) < abs(x_max):
        x_values.append(round(x, 3))
        x += step

    return x_values


def print_res_table(x_values, u_values_by_picar1, u_values_by_picar2,
                    u_values_by_picar3, u_values_by_picar4, u_values_by_euler):
    """
    Функция для вывода таблицы согласно заданию
    """

    print(f'\n| {"x": ^7} | {"picard1": ^22} | {"picard2": ^22} | {"picard3": ^22} |'
          f' {"picard4": ^22} | {"euler": ^22} |')
    print("-" * 136)

    for i in range(len(x_values)):
        if i % 500 == 0:
            print(f"| {x_values[i]: ^7.3f} | {u_values_by_picar1[i]: ^22.3f} | {u_values_by_picar2[i]: ^22.3f} |"
                  f" {u_values_by_picar3[i]: ^22.3f} | {u_values_by_picar4[i]: ^22.3f} |"
                  f" {u_values_by_euler[i]: ^22.3f} |")

    print("-" * 136)
    print()


def build_graph(x_values, u_values_by_picar1, u_values_by_picar2,
                u_values_by_picar3, u_values_by_picar4, u_values_by_euler):
    """
    Функция для вывода графика (для себя)
    """
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(10, 7))

    axs[0].plot(x_values, u_values_by_picar1, label="picard1")
    axs[0].plot(x_values, u_values_by_picar2, label="picard2")
    axs[0].plot(x_values, u_values_by_picar3, label="picard3")
    axs[0].plot(x_values, u_values_by_picar4, label="picard4")
    axs[0].set_xlabel("x")
    axs[0].set_ylabel("u(x)")
    axs[0].legend()
    axs[0].grid(True)

    axs[1].plot(x_values, u_values_by_picar1, label="picard1")
    axs[1].plot(x_values, u_values_by_picar2, label="picard2")
    axs[1].plot(x_values, u_values_by_picar3, label="picard3")
    axs[1].plot(x_values, u_values_by_picar4, label="picard4")
    axs[1].plot(x_values, u_values_by_euler, label="euler")
    axs[1].set_xlabel("x")
    axs[1].set_ylabel("u(x)")
    axs[1].legend()
    axs[1].grid(True)

    plt.show()


def get_solution() -> None:
    """
    Функция выводит все решения задачи
    """
    x_values: list[int | float] = get_generate_x(MAX_X, STEP)

    u_values_by_picar1: list[int | float] = get_picard_approx(MAX_X, STEP, get_u_x_by_picard1)
    u_values_by_picar2: list[int | float] = get_picard_approx(MAX_X, STEP, get_u_x_by_picard2)
    u_values_by_picar3: list[int | float] = get_picard_approx(MAX_X, STEP, get_u_x_by_picard3)
    u_values_by_picar4: list[int | float] = get_picard_approx(MAX_X, STEP, get_u_x_by_picard4)

    u_values_by_euler: list[int | float] = get_euler_approx(MAX_X, STEP)

    print_res_table(x_values, u_values_by_picar1, u_values_by_picar2,
                    u_values_by_picar3, u_values_by_picar4, u_values_by_euler)

    build_graph(x_values, u_values_by_picar1, u_values_by_picar2,
                u_values_by_picar3, u_values_by_picar4, u_values_by_euler)
