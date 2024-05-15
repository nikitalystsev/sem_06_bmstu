import numpy as np
from dataclasses import dataclass
import matplotlib.pyplot as plt

EPS = 1e-4


@dataclass
class TaskOps:
    """
    Класс параметров задачи
    """
    # константы лабы
    k0: int | float = 1.0  # ок
    a1: int | float = 0.0134  # ок
    b1: int | float = 1  # ок
    c1: int | float = 4.35e-4  # ок
    m1: int | float = 1  # ок
    a2: int | float = 2.049  # ок
    b2: int | float = 0.563e-3  # ок
    c2: int | float = 0.528e5  # ок
    m2: int | float = 1  # ок
    l: int | float = 10  # ок
    t0: int | float = 300  # ок
    r: int | float = 0.5  # ок

    alpha_0: int | float = 0.05  # ок в x = 0
    alpha_n: int | float = 0.01  # ок в x = l

    d: int | float = 0.01 * l / (-0.04)  # ок
    c: int | float = -0.05 * d  # ок

    # для отладки принять
    f_max: int | float = 50  # ок
    t_max: int | float = 60  # ок


@dataclass(frozen=True)
class Grid:
    """
    Класс -- хранитель числа узлов, шагов по каждой переменной
    (сетка, крч)
    """
    a: int | float
    b: int | float
    n: int
    h: int | float
    time0: int | float
    timem: int | float
    m: int
    tau: int | float


def alpha(x, ops: TaskOps):
    """
    Функция альфа (вроде правильно)
    """
    c, d = ops.c, ops.d

    return c / (x - d)


def _lambda(t, ops: TaskOps):
    """
    Функция λ(T) (вроде правильно)
    """
    a1, b1, c1, m1 = ops.a1, ops.b1, ops.c1, ops.m1

    return a1 * (b1 + c1 * t ** m1)


def _c(t, ops: TaskOps):
    """
    Функция c(T) (вроде правильно)
    """
    a2, b2, c2, m2 = ops.a2, ops.b2, ops.c2, ops.m2

    return a2 + b2 * t ** m2 - (c2 / (t ** 2))


def k(t, ops: TaskOps):
    """
    Функция k(T) (вроде правильно)
    """
    k0 = ops.k0

    return k0 * (t / 300) ** 2


def f0(time, ops: TaskOps):
    """
    Функция потока излучения F0(t) при x = 0 (вроде правильно)
    """
    f_max, t_max = ops.f_max, ops.t_max

    # return (f_max / t_max) * time * np.exp(-((time / t_max) - 1))
    return 20


def p(x, ops: TaskOps):
    """
    Функция p(u) для исходного уравнения (вроде правильно)
    """
    r = ops.r

    return (2 / r) * alpha(x, ops)


def f(x, time, t, ops: TaskOps):
    """
    Функция f(T) для исходного уравнения
    t = t(x, time) (вроде правильно)
    """
    t0, r = ops.t0, ops.r

    return k(t, ops) * f0(time, ops) * np.exp(-k(t, ops) * x) + (2 * t0 / r) * alpha(x, ops)


def kappa(t1, t2, ops: TaskOps):
    """
    Функция каппа (вычисляется с использованием метода средних)
    """

    return (_lambda(t1, ops) + _lambda(t2, ops)) / 2


def left_boundary_condition(t_m, curr_time, data: Grid, ops: TaskOps):
    """
    Левое краевое условие прогонки
    """
    a, h, tau = data.a, data.h, data.tau
    alpha_0, t0 = ops.alpha_0, ops.t0

    k_0 = (h / 8) * _c((t_m[0] + t_m[1]) / 2, ops) + \
          (h / 4) * _c(t_m[0], ops) + kappa(t_m[0], t_m[1], ops) * tau / h + \
          (h * tau / 8) * p(a + h / 2, ops) + \
          (h * tau / 4) * p(a, ops) + alpha_0 * tau

    m_0 = (h / 8) * _c((t_m[0] + t_m[1]) / 2, ops) - \
          (tau / h) * kappa(t_m[0], t_m[1], ops) + \
          (h * tau / 8) * p(a + h / 2, ops)

    p_0 = (h / 8) * _c((t_m[0] + t_m[1]) / 2, ops) * (t_m[0] + t_m[1]) + \
          (h / 4) * _c(t_m[0], ops) * t_m[0] + tau * alpha_0 * t0 + \
          (tau * h / 4) * (f(0, curr_time, t_m[0], ops) +
                           f(0, curr_time, t_m[0] + t_m[1] / 2, ops))

    return k_0, m_0, p_0


def right_boundary_condition(t_m, curr_time, data: Grid):
    """
    Правое краевое условие прогонки
    """
    b, h, tau = data.b, data.h, data.tau

    k_n = (h / 8) * _c((t_m[-1] + t_m[-2]) / 2) - \
          (tau / h) * kappa(t_m[-2], t_m[-1]) + \
          (h / 8) * p(b - h / 2) * tau

    m_n = (h / 4) * _c(t_m[-1]) + \
          (h / 8) * _c((t_m[-1] + t_m[-2]) / 2) + \
          (tau / h) * kappa(t_m[-2], t_m[-1]) + \
          tau * alpha_n + (h * tau / 8) * p(b - h / 2) + \
          (h * tau / 4) * p(b)

    p_n = (h / 4) * _c(t_m[-1]) * t_m[-1] + \
          (h / 8) * _c((t_m[-1] + t_m[-2]) / 2) * t_m[-2] + \
          (h / 8) * _c((t_m[-1] + t_m[-2]) / 2) * t_m[-1] + \
          t0 * tau * alpha_n + \
          (h * tau / 4) * (f(b - h / 2, curr_time, (t_m[-2] + t_m[-1]) / 2) +
                           f(b, curr_time, t_m[-1]))

    return k_n, m_n, p_n


def right_sweep(t_m, curr_time, data: Grid):
    """
    Реализация правой прогонки
    """
    b, h, tau = data.b, data.h, data.tau
    # Прямой ход
    k_0, m_0, p_0 = left_boundary_condition(t_m, curr_time, data)
    k_n, m_n, p_n = right_boundary_condition(t_m, curr_time, data)

    ksi = [0, -m_0 / k_0]
    eta = [0, p_0 / k_0]

    x = h
    n = 1

    for i in range(1, len(t_m) - 1):
        a_n = kappa(t_m[i - 1], t_m[i]) * tau / h
        d_n = kappa(t_m[i], t_m[i + 1]) * tau / h
        b_n = a_n + d_n + _c(t_m[i]) * h + p(x) * h * tau
        f_n = _c(t_m[i]) * t_m[i] * h + f(x, curr_time, t_m[i]) * h * tau

        ksi.append(d_n / (b_n - a_n * ksi[n]))
        eta.append((a_n * eta[n] + f_n) / (b_n - a_n * ksi[n]))

        n += 1
        x += h

    # Обратный ход
    u = [0] * (n + 1)

    u[n] = (p_n - k_n * eta[n]) / (k_n * ksi[n] + m_n)

    for i in range(n - 1, -1, -1):
        u[i] = ksi[i + 1] * u[i + 1] + eta[i + 1]

    return u


def simple_iteration_on_layer(t_m, curr_time, data):
    """
    Вычисляет значение искомой функции (функции T) на слое t_m_plus_1
    """
    _t_m = t_m
    while True:
        # цикл подсчета значений функции T методом простых итераций для
        # слоя t_m_plus_1
        t_m_plus_1 = right_sweep(_t_m, curr_time, data)

        cnt = 0

        for i in range(len(_t_m)):
            curr_err = abs((_t_m[i] - t_m_plus_1[i]) / t_m_plus_1[i])
            if curr_err < EPS:
                cnt += 1

        if cnt == len(_t_m):
            break

        _t_m = t_m_plus_1

    return t_m_plus_1


def simple_iteration(data: Grid):
    """
    Реализация метода простых итераций для решения нелинейной системы уравнений
    """
    n = int((data.b - data.a) / data.h)  # число узлов по координате
    t = [t0 for _ in range(n)]  # начальное условие

    t_m = t

    t_res = []

    curr_time = data.time0

    while curr_time <= data.timem:
        # цикл подсчета значений функции T
        t_m_plus_1 = simple_iteration_on_layer(t_m, curr_time, data)

        t_res.append(t_m_plus_1)

        curr_time += data.tau

        t_m = t_m_plus_1

    return t_res


def main() -> None:
    """
    Главная функция
    """
    a, b = 0, l  # диапазон значений координаты
    n = 1000
    h = (b - a) / n
    time0, timem = 0, 100  # диапазон значений времени
    m = 100
    tau = (timem - time0) / m

    data = Grid(a, b, n, h, time0, timem, m, tau)

    t_res = np.array(simple_iteration(data))[:-1]

    x = np.arange(a, b, h)
    t = np.arange(time0, timem, tau)

    X, T = np.meshgrid(x, t)

    # Построение графика
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, T, t_res, cmap='viridis')

    # Настройка подписей осей
    ax.set_xlabel('x')
    ax.set_ylabel('t')
    ax.set_zlabel('T(x, t)')
    ax.set_title('Температурное поле')

    # Показать график
    plt.show()


if __name__ == '__main__':
    main()
