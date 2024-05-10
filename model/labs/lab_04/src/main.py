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

EPS = 1e-4


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


def p(x):
    """
    Функция p(u) для исходного уравнения
    """

    return (2 / r) * alpha(x)


def f(x, time, t):
    """
    Функция f(x, u) для исходного уравнения
    идейно, пока что, t - массив значений функции T в текущий момент времени
    """

    return k(t[x]) * f0(time) * np.exp(-k(t[x]) * x) + (2 * t0 / r) * alpha(x)


def kappa(t1, t2):
    """
    Функция каппа (вычисляется с использованием метода средних)
    """

    return (_lambda(t1) + _lambda(t2)) / 2


def left_boundary_condition(z0, g0, h):
    """
    Левое краевое условие метода правой прогонки
    """


def solve(t):
    """
    Функция получения решения прогонкой
    """

    return t  # пока что


def simple_iteration_on_layer(t_m):
    """
    Вычисляет значение искомой функции (функции T) на слое t_m_plus_1
    """
    _t_m = t_m
    while True:
        # цикл подсчета значений функции T методом простых итераций для
        # слоя t_m_plus_1
        t_m_plus_1 = solve(_t_m)

        cnt = 0

        for i in range(len(_t_m)):
            curr_err = abs((_t_m[i] - t_m_plus_1[i]) / t_m_plus_1[i])
            if curr_err < EPS:
                cnt += 1

        if cnt == len(_t_m):
            break

        _t_m = t_m_plus_1

    return t_m_plus_1


def simple_iteration(a, b, h, time0, timem, tau):
    """
    Реализация метода простых итераций для решения нелинейной системы уравнений
    """
    n = int((b - a) / h)  # число узлов по координате
    t = [t0 for _ in range(n)]  # начальное условие

    t_m = t

    t_res = []

    tmp = time0

    while tmp <= timem:
        # цикл подсчета значений функции T
        t_m_plus_1 = simple_iteration_on_layer(t_m)

        t_res.append(t_m_plus_1)

        tmp += tau

        t_m = t_m_plus_1

    return t_res


def main() -> None:
    """
    Главная функция
    """
    a, b = 0, l  # диапазон значений координаты
    n = 10
    h = (b - a) / n
    time0, timem = 0, 100  # диапазон значений времени
    m = 10
    tau = (timem - time0) / m

    t_res = simple_iteration(a, b, h, time0, timem, tau)

    print(t_res)


if __name__ == '__main__':
    main()
