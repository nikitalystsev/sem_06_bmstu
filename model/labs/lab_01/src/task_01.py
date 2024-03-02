import numpy as np
import matplotlib.pyplot as plt


# u'' + 0.1 * (u')^2 + (1 + 0.1 * x) * u = 0
# u(0) = 1, u'(0) = 2

# раскладываем в ряд Тейлора и находим коэффициенты при первых 5-ти членах

def get_first() -> int:
    """
    Функция возвращает первый член ряда Тейлора
    """

    return 1


def get_second() -> int:
    """
    Функция возвращает производную при втором члене ряда Тейлора
    """

    return 2


def get_third(x_0: float) -> float:
    """
    Функция возвращает производную при третьем члене ряда Тейлора
    """

    _sum = 0.1 * (get_second() ** 2) + (1 + 0.1 * x_0) * get_first()

    return -_sum


def get_fourth(x_0: float) -> float:
    """
    Функция возвращает производную при четвертом члене ряда Тейлора
    """

    _sum = 0.1 * 2 * get_second() * get_third(x_0) + get_second() + 0.1 * (get_first() + x_0 * get_second())

    return -_sum


def get_fifth(x_0: float) -> float:
    """
    Функция возвращает производную при пятом члене ряда Тейлора
    """

    _sum = 0.2 * (get_third(x_0) ** 2 + get_second() * get_fourth(x_0)) + get_third(x_0) + 0.1 * get_second() + \
           0.1 * (get_second() + x_0 * get_third(x_0))

    return -_sum


def get_u_x_by_row(x_0: float):
    """
    Функция выводит на экран функцию u
    """

    str_u_x = f"Разложением в ряд: u(x) = {get_first()} + {get_second() / 1: .3f} * x + " \
              f"{get_third(x_0) / 2: .3f} * x^2 +" \
              f" {get_fourth(x_0) / 6: .3f} * x^3 + " \
              f"{get_fifth(x_0) / 24: .3f} * x^4"

    print(str_u_x)

    def f(x: int | float | np.ndarray) -> int | float | np.ndarray:
        return get_first() + (get_second() / 1) * x + \
            (get_third(x_0) / 2) * x ** 2 + \
            (get_fourth(x_0) / 6) * x ** 3 + \
            (get_fifth(x_0) / 24) * x ** 4

    return f


def get_u_x_by_euler():
    """
    Функция выводит на экран функцию u методом Эйлера
    """

    str_u_x_by_euler = f"Методом Эйлера: u(x) = {get_first()} + {get_second() / 1} * x"

    print(str_u_x_by_euler)

    def f(x: int | float | np.ndarray) -> int | float | np.ndarray:
        return get_first() + get_second() / 1 * x

    return f


def get_u_x_by_picard1():
    """
    Функция выводит на экран функцию u методом Пикара (1-е приближение)
    """

    str_u_x_by_picard1 = f"Методом Пикара: u(x) = 2 - 1.40 * x - 0.05 * x^2 + 1"

    print(str_u_x_by_picard1)

    def f(x: int | float | np.ndarray) -> int | float | np.ndarray:
        return - (x ** 3) / 60 - (7 * (x ** 2)) / 10 + 2 * x + 1

    return f


def get_u_x_by_picard2():
    """
    Функция выводит на экран функцию u методом Пикара (2-е приближение)
    """

    def f(x: int | float | np.ndarray) -> int | float | np.ndarray:
        return - (x ** 3) / 60 - (x ** 2) / 2 + (158 * x) / 87 - (40 - 29 * x) ** 4 / 40368000 + 1 + 40 ** 4 / 40368000

    return f


def get_solution() -> None:
    """
    Функция выводит все решения задачи
    """
    f_row = get_u_x_by_row(0)
    f_euler = get_u_x_by_euler()
    f_picard1 = get_u_x_by_picard1()
    f_picard2 = get_u_x_by_picard2()

    x_values: np.ndarray | tuple[np.ndarray, float | None] = np.linspace(-2, 6, 100)
    y_values_picard2: np.ndarray | tuple[np.ndarray, float | None] = f_picard2(x_values)
    y_values_row: np.ndarray | tuple[np.ndarray, float | None] = f_row(x_values)
    y_values_euler: np.ndarray | tuple[np.ndarray, float | None] = f_euler(x_values)

    fig1 = plt.figure(figsize=(10, 7))
    plot = fig1.add_subplot()

    plot.plot(x_values, y_values_picard2, label="Метод Пикара (2-е приближение)")
    plot.plot(x_values, y_values_row, label="Разложение в ряд Тейлора (первые 5 членов)")
    plot.plot(x_values, y_values_euler, label="Метод Эйлера")

    plt.legend()
    plt.grid()
    plt.title("Сравнение методов")

    plt.show()

    # x_min = min(x_values)
    # x_max = max(x_values)
    # y_min = min(min(y_values_picard2), min(y_values_row))
    # y_max = max(max(y_values_picard2), max(y_values_row))
    #
    # fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(10, 5))
    #
    # # Постройте первый график
    # axs[0].plot(x_values, y_values_picard2, color='blue')
    # axs[0].set_title('Метод Пикара (2-е приближение)')
    # axs[0].set_xlim(x_min, x_max)
    # axs[0].set_ylim(y_min, y_max)
    # axs[0].grid(True)
    #
    # # Постройте второй график
    # axs[1].plot(x_values, y_values_row, color='red')
    # axs[1].set_title('Разложение в ряд Тейлора (первые 5 членов)')
    # axs[1].set_xlim(x_min, x_max)
    # axs[1].set_ylim(y_min, y_max)
    # axs[1].grid(True)
    #
    # # Постройте второй график
    # axs[2].plot(x_values, y_values_euler, color='red')
    # axs[2].set_title('Метод Эйлера')
    # axs[2].set_xlim(x_min, x_max)
    # axs[2].set_ylim(y_min, y_max)
    # axs[2].grid(True)

    # # Отобразите все графики
    # plt.tight_layout()  # Распределить графики равномерно по окну
    # plt.show()

    try:
        arg = float(input("Введите значение аргумента: "))
    except ValueError:
        print("Неверный ввод!")
        return

    print(f"Решение разложением в ряд Тейлора (первые 5 членов):  u({arg}) = ", f_row(arg))
    print(f"Решение методом Эйлера:                               u({arg}) = ", f_euler(arg))
    print(f"Решение методом Пикара (1-е приближение):             u({arg}) = ", f_picard1(arg))
    print(f"Решение методом Пикара (2-е приближение):             u({arg}) = ", f_picard2(arg))
