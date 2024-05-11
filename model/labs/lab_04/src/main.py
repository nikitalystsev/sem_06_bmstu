import numpy as np
from dataclasses import dataclass
import matplotlib.pyplot as plt

# константы лабы
k0 = 1.0  # ок
a1 = 0.0134  # ок
b1 = 1  # ок
c1 = 4.35e-4  # ок
m1 = 1  # ок
a2 = 2.049  # ок
b2 = 0.563e-3  # ок
c2 = 0.528e5  # ок
m2 = 1  # ок
l = 10  # ок
t0 = 300  # ок
r = 0.5  # ок

alpha_0 = 0.05  # ок в x = 0
alpha_n = 0.01  # ок в x = l

d = 0.01 * l / (-0.04)  # ок
c = -0.05 * d  # ок

# для отладки принять
f_max = 50  # ок
t_max = 60  # ок

EPS = 1e-4


@dataclass(frozen=True)
class Data:
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


def alpha(x):
    """
    Функция альфа (вроде правильно)
    """

    return c / (x - d)


def _lambda(t):
    """
    Функция λ(T) (вроде правильно)
    """

    return a1 * (b1 + c1 * t ** m1)


def _c(t):
    """
    Функция c(T) (вроде правильно)
    """

    return a2 + b2 * t ** m2 - (c2 / (t ** 2))


def k(t):
    """
    Функция k(T) (вроде правильно)
    """

    return k0 * (t / 300) ** 2


def f0(time):
    """
    Функция потока излучения F0(t) при x = 0 (вроде правильно)
    """

    return (f_max / t_max) * time * np.exp(-((time / t_max) - 1))


def p(x):
    """
    Функция p(u) для исходного уравнения (вроде правильно)
    """

    return (2 / r) * alpha(x)


def f(x, time, t):
    """
    Функция f(T) для исходного уравнения
    t = t(x, time) (вроде правильно)
    """

    return k(t) * f0(time) * np.exp(-k(t) * x) + (2 * t0 / r) * alpha(x)


def kappa(t1, t2):
    """
    Функция каппа (вычисляется с использованием метода средних)
    """

    return (_lambda(t1) + _lambda(t2)) / 2


def left_boundary_condition(t_m, curr_time, data: Data):
    """
    Левое краевое условие прогонки
    """
    a, h, tau = data.a, data.h, data.tau

    # вроде ок
    k_0 = (h / 8) * _c((t_m[0] + t_m[1]) / 2) + \
          (h / 4) * _c(t_m[0]) + kappa(t_m[0], t_m[1]) * tau / h + \
          (h * tau / 8) * p(a + h / 2) + \
          (h * tau / 4) * p(a) - alpha_0 * tau

    # вроде ок
    m_0 = (h / 8) * _c((t_m[0] + t_m[1]) / 2) - \
          (tau / h) * kappa(t_m[0], t_m[1]) + \
          (h * tau / 8) * p(a + h / 2)

    # вроде ок
    p_0 = (h / 8) * _c((t_m[0] + t_m[1]) / 2) * (t_m[0] + t_m[1]) + \
          (h / 4) * _c(t_m[0]) * t_m[0] - alpha_0 * t0 * tau + \
          (tau * h / 4) * (f(0, curr_time, t_m[0]) +
                           f(0, curr_time, t_m[0] + t_m[1] / 2))

    return k_0, m_0, p_0


def right_boundary_condition(t_m, curr_time, data: Data):
    """
    Правое краевое условие прогонки
    """
    b, h, tau = data.b, data.h, data.tau

    # вроде ок
    k_n = (h / 8) * _c((t_m[-1] + t_m[-2]) / 2) - \
          (tau / h) * kappa(t_m[-2], t_m[-1]) + \
          (h / 8) * p(b - h / 2) * tau

    # вроде ок
    m_n = (h / 4) * _c(t_m[-1]) + \
          (h / 8) * _c((t_m[-1] + t_m[-2]) / 2) + \
          (tau / h) * kappa(t_m[-2], t_m[-1]) + \
          tau * alpha_n + (h * tau / 8) * p(b - h / 2) + \
          (h * tau / 4) * p(b)

    # вроде ок
    p_n = (h / 4) * _c(t_m[-1]) * t_m[-1] + \
          (h / 8) * _c((t_m[-1] + t_m[-2]) / 2) * t_m[-2] + \
          (h / 8) * _c((t_m[-1] + t_m[-2]) / 2) * t_m[-1] + \
          t0 * tau * alpha_n + \
          (h * tau / 4) * (f(b - h / 2, curr_time, (t_m[-2] + t_m[-1]) / 2) +
                           f(b, curr_time, t_m[-1]))

    return k_n, m_n, p_n


def right_sweep(t_m, curr_time, data: Data):
    """
    Реализация правой прогонки
    """
    b, h, tau = data.b, data.h, data.tau
    # Прямой ход
    k_0, m_0, p_0 = left_boundary_condition(t_m, curr_time, data)
    k_n, m_n, p_n = right_boundary_condition(t_m, curr_time, data)

    ksi = [0, -k_0 / m_0]
    eta = [0, p_0 / m_0]

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
    # print("[+] call simple_iteration_on_layer")
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

    # print("[+] return simple_iteration_on_layer")

    return t_m_plus_1


def simple_iteration(data: Data):
    """
    Реализация метода простых итераций для решения нелинейной системы уравнений
    """
    # print("[+] call simple_iteration")
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

    # print("[+] return simple_iteration")

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

    data = Data(a, b, n, h, time0, timem, m, tau)

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
