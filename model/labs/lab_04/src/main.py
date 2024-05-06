import numpy as np

# константы лабы
k0 = 1.0
a1 = 0.0134
b1 = 1
c1 = 4.35e-4
m1 = 1
a2 = 2.049
b2 = 0.563e-3
c2 = 0.528e5
m2 = 1
l = 10
t0 = 300
r = 0.5

"""
alpha0 = 0.05 в точке x0
alphaN = 0.01 в точке xN
"""
d = 0.01 * l / (-0.04)
c = -0.05 * d

# для отладки принять
f_max = 50
t_max = 60


def alpha(x):
    """
    Функция альфа
    """

    return c / (x - d)


def _lambda(t):
    """
    Функция λ(T)
    """

    return a1 * (b1 + c1 * t ** m1)


def _c(t):
    """
    Функция c(T)
    """

    return a2 + b2 * t ** m2 - c2 / (t ** 2)


def k(t):
    """
    Функция k(T)
    """

    return k0 * (t / 300) ** 2


def f0(time):
    """
    Функция потока излучения F0(t) при x = 0
    """

    return (f_max / t_max) * time * np.exp(-((time / t_max) - 1))


def main() -> None:
    """
    Главная функция
    """


if __name__ == '__main__':
    main()
