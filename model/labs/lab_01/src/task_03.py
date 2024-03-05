import matplotlib.pyplot as plt
from typing import Callable
import numpy as np

EPS = 1e-4


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


def get_picard_approx(x_values: np.ndarray, u_x_by_picard_func: Callable[[int | float], int | float]) -> dict:
    """
    Функция для получения массива значений функции методом Пикара переданного приближения
    """
    u_values = dict()

    u = 0

    for x in x_values:
        u_values[x] = u
        u = u_x_by_picard_func(x)

    return u_values


def get_euler_approx(x_values: np.ndarray, h: int | float) -> dict:
    """
    Функция для получения массива значений функции методом Эйлера
    """
    u_values = dict()

    u = 0

    for x in x_values:
        u_values[x] = u
        u = u + h * f(x, u)

    return u_values


def calc_error(u1_h: int | float, u1_h_half_2: int | float):
    """
    Функция для вычисления относительной погрешности
    :param u1_h: условно точное значение
    :param u1_h_half_2: условно приближенное значение
    """

    return np.abs(u1_h - u1_h_half_2) / (np.abs(u1_h_half_2) + 1e-10)


def find_xmax() -> (int | float, int | float):
    """
    Функция поиска xmax
    """
    xmax = 2.5  # начальное значение
    step = 0.1  # начальное значение шага

    while xmax >= 2:
        step = 0.1  # начальное значение шага
        while step >= 1e-6:

            x_values1: np.ndarray = np.arange(0, xmax + step, step)
            x_values2: np.ndarray = np.arange(0, xmax + step, step / 2)

            u_values_by_euler1: dict = get_euler_approx(x_values1, step)
            u_values_by_euler2: dict = get_euler_approx(x_values2, step / 2)

            count = 0

            for x in x_values1[1:]:
                error = calc_error(u_values_by_euler1[x], u_values_by_euler2[x])
                # print(f"error = {error}")

                if error < EPS:
                    count += 1

            # print(f"count = {count}")
            # print(f"len(x_values1) - 1 = {len(x_values1) - 1}")

            if count == len(x_values1) - 1:
                break

            step /= 2
        print(f"xmax = {xmax}")
        xmax -= 0.01

    return xmax, step


def print_res_table(x_values, u_values_by_picar1, u_values_by_picar2,
                    u_values_by_picar3, u_values_by_picar4, u_values_by_euler):
    """
    Функция для вывода таблицы согласно заданию
    """

    print(f'\n| {"x": ^7} | {"picard1": ^22} | {"picard2": ^22} | {"picard3": ^22} |'
          f' {"picard4": ^22} | {"euler": ^22} |')
    print("-" * 136)

    for x in x_values:
        print(f"| {x: ^7.5f} | {u_values_by_picar1[x]: ^22.5f} | {u_values_by_picar2[x]: ^22.5f} |"
              f" {u_values_by_picar3[x]: ^22.5f} | {u_values_by_picar4[x]: ^22.5f} |"
              f" {u_values_by_euler[x]: ^22.5f} |")

    print("-" * 136)
    print()


def build_graph(x_values, u_values_by_picar1, u_values_by_picar2,
                u_values_by_picar3, u_values_by_picar4, u_values_by_euler):
    """
    Функция для вывода графика (для себя)
    """
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(10, 7))

    axs[0].plot(x_values, u_values_by_picar1.values(), label="picard1")
    axs[0].plot(x_values, u_values_by_picar2.values(), label="picard2")
    axs[0].plot(x_values, u_values_by_picar3.values(), label="picard3")
    axs[0].plot(x_values, u_values_by_picar4.values(), label="picard4")
    axs[0].set_xlabel("x")
    axs[0].set_ylabel("u(x)")
    axs[0].legend()
    axs[0].grid(True)

    axs[1].plot(x_values, u_values_by_picar1.values(), label="picard1")
    axs[1].plot(x_values, u_values_by_picar2.values(), label="picard2")
    axs[1].plot(x_values, u_values_by_picar3.values(), label="picard3")
    axs[1].plot(x_values, u_values_by_picar4.values(), label="picard4")
    axs[1].plot(x_values, u_values_by_euler.values(), label="euler")
    axs[1].set_xlabel("x")
    axs[1].set_ylabel("u(x)")
    axs[1].legend()
    axs[1].grid(True)

    plt.show()


def get_solution() -> None:
    """
    Функция выводит все решения задачи
    """
    # xmax, step = find_xmax()
    # print(f"xmax = {xmax}, step = {step}")

    xmax = 2.14
    step = 0.01

    x_values: np.ndarray = np.arange(0, xmax, step)

    u_values_by_picar1: dict = get_picard_approx(x_values, get_u_x_by_picard1)
    u_values_by_picar2: dict = get_picard_approx(x_values, get_u_x_by_picard2)
    u_values_by_picar3: dict = get_picard_approx(x_values, get_u_x_by_picard3)
    u_values_by_picar4: dict = get_picard_approx(x_values, get_u_x_by_picard4)

    u_values_by_euler: dict = get_euler_approx(x_values, step)

    print_res_table(x_values, u_values_by_picar1, u_values_by_picar2,
                    u_values_by_picar3, u_values_by_picar4, u_values_by_euler)

    build_graph(x_values, u_values_by_picar1, u_values_by_picar2,
                u_values_by_picar3, u_values_by_picar4, u_values_by_euler)
