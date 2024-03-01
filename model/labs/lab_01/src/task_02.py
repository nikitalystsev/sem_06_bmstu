import math as m


# 1 - 2 * x * u * u' = u ^ 3 * u'
# u(0.5) = 0

def get_x_u_by_analyt(u: int | float) -> int | float:
    """
    Функция аналитического решения
    """

    return m.exp(u ** 2) - (u ** 2) / 2 - 1 / 2


def get_x_u_by_picard1(u: int | float) -> int | float:
    """
    Функция решения методом Пикара (1-е приближение)
    """

    return 0.5 + (u ** 2) / 2 + (u ** 4) / 4


def get_x_u_by_picard2(u: int | float) -> int | float:
    """
    Функция решения методом Пикара (2-е приближение)
    """

    return 0.5 + (u ** 16) / 12 + (u ** 4) / 2 + (u ** 2) / 2


def get_x_u_by_picard3(u: int | float) -> int | float:
    """
    Функция решения методом Пикара (3-е приближение)
    """

    return 0.5 + (u ** 18) / 108 + (u ** 6) / 6 + (u ** 4) / 2 + (u ** 2) / 2


def get_x_u_by_picard4(u: int | float) -> int | float:
    """
    Функция решения методом Пикара (4-е приближение)
    """

    return 0.5 + (u ** 20) / 1080 + (u ** 8) / 24 + (u ** 6) / 6 + (u ** 4) / 2 + (u ** 2) / 2


def get_x_u_by_picard5(u: int | float) -> int | float:
    """
    Функция решения методом Пикара (4-е приближение)
    """

    return 0.5 + (u ** 22) / 1080 + (u ** 10) / 24 + (u ** 8) / 6 + (u ** 6) / 2 + 3 * (u ** 4) / 4 + (u ** 2) / 2
