import numpy as np
from dataclasses import dataclass
import matplotlib.pyplot as plt
from copy import copy

EPS = 1e-4

curr_count = 1

is_f0_const = False


# is_f0_const = True


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
    t_max: int | float = 5  # ок


@dataclass
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

    if is_f0_const:
        return 10

    # h = t_max * 3.5
    #
    # if time < h:
    #     return (f_max / t_max) * time * np.exp(-((time / t_max) - 1))
    # else:
    #     coef = time // h
    #     t = time - h * coef
    #     return (f_max / t_max) * t * np.exp(-((t / t_max) - 1))

    return (f_max / t_max) * time * np.exp(-((time / t_max) - 1))


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


def left_boundary_condition(_t_m, __t_m, curr_time, data: Grid, ops: TaskOps):
    """
    Левое краевое условие прогонки
    """
    # __t_m -- с крышкой (текущие)
    a, h, tau = data.a, data.h, data.tau
    alpha_0, t0 = ops.alpha_0, ops.t0

    k_0 = (h / 8) * _c((__t_m[0] + __t_m[1]) / 2, ops) + \
          (h / 4) * _c(__t_m[0], ops) + kappa(__t_m[0], __t_m[1], ops) * tau / h + \
          (h * tau / 8) * p(a + h / 2, ops) + \
          (h * tau / 4) * p(a, ops) + alpha_0 * tau

    m_0 = (h / 8) * _c((__t_m[0] + __t_m[1]) / 2, ops) - \
          (tau / h) * kappa(__t_m[0], __t_m[1], ops) + \
          (h * tau / 8) * p(a + h / 2, ops)

    p_0 = (h / 8) * _c((__t_m[0] + __t_m[1]) / 2, ops) * (_t_m[0] + _t_m[1]) + \
          (h / 4) * _c(__t_m[0], ops) * _t_m[0] + tau * alpha_0 * t0 + \
          (tau * h / 4) * (f(0, curr_time, __t_m[0], ops) +
                           f(0, curr_time, (__t_m[0] + __t_m[1]) / 2, ops))

    return k_0, m_0, p_0


def right_boundary_condition(_t_m, __t_m, curr_time, data: Grid, ops: TaskOps):
    """
    Правое краевое условие прогонки
    """
    b, h, tau = data.b, data.h, data.tau
    alpha_n, t0 = ops.alpha_n, ops.t0

    k_n = (h / 8) * _c((__t_m[-1] + __t_m[-2]) / 2, ops) - \
          (tau / h) * kappa(__t_m[-2], __t_m[-1], ops) + \
          (h / 8) * p(b - h / 2, ops) * tau

    m_n = (h / 4) * _c(__t_m[-1], ops) + \
          (h / 8) * _c((__t_m[-1] + __t_m[-2]) / 2, ops) + \
          (tau / h) * kappa(__t_m[-2], __t_m[-1], ops) + tau * alpha_n + \
          (h * tau / 8) * p(b - h / 2, ops) + \
          (h * tau / 4) * p(b, ops)

    p_n = (h / 4) * _c(__t_m[-1], ops) * _t_m[-1] + \
          (h / 8) * _c((__t_m[-1] + __t_m[-2]) / 2, ops) * (_t_m[-2] + _t_m[-1]) + t0 * tau * alpha_n + \
          (h * tau / 4) * (f(b - h / 2, curr_time, (__t_m[-2] + __t_m[-1]) / 2, ops) +
                           f(b, curr_time, __t_m[-1], ops))

    return k_n, m_n, p_n


def right_sweep(_t_m, __t_m, curr_time, data: Grid, ops: TaskOps):
    """
    Реализация правой прогонки
    """
    b, h, tau = data.b, data.h, data.tau
    # Прямой ход
    k_0, m_0, p_0 = left_boundary_condition(_t_m, __t_m, curr_time, data, ops)
    k_n, m_n, p_n = right_boundary_condition(_t_m, __t_m, curr_time, data, ops)

    ksi = [0, -m_0 / k_0]
    eta = [0, p_0 / k_0]

    x = h
    n = 1

    for i in range(1, len(__t_m) - 1):
        a_n = kappa(__t_m[i - 1], __t_m[i], ops) * tau / h
        d_n = kappa(__t_m[i], __t_m[i + 1], ops) * tau / h
        b_n = a_n + d_n + _c(__t_m[i], ops) * h + p(x, ops) * h * tau
        f_n = _c(__t_m[i], ops) * _t_m[i] * h + f(x, curr_time, __t_m[i], ops) * h * tau

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


def simple_iteration_on_layer(t_m, curr_time, data: Grid, ops: TaskOps):
    """
    Вычисляет значение искомой функции (функции T) на слое t_m_plus_1
    """
    _t_m = t_m  # предыдущие (без крышки)
    __t_m = t_m  # текущие (с крышкой)

    while True:
        # цикл подсчета значений функции T методом простых итераций для
        # слоя t_m_plus_1
        t_m_plus_1 = right_sweep(_t_m, __t_m, curr_time, data, ops)

        cnt = 0

        for i in range(len(_t_m)):
            curr_err = abs((__t_m[i] - t_m_plus_1[i]) / t_m_plus_1[i])
            if curr_err < EPS:
                cnt += 1

        if cnt == len(__t_m):
            break

        __t_m = t_m_plus_1

    return t_m_plus_1


def simple_iteration(data: Grid, ops: TaskOps):
    """
    Реализация метода простых итераций для решения нелинейной системы уравнений
    """
    n = int((data.b - data.a) / data.h)  # число узлов по координате
    t = [ops.t0 for _ in range(n + 1)]  # начальное условие

    x = np.arange(data.a, data.b + data.h, data.h)
    times = np.arange(data.time0, data.timem + data.tau, data.tau)

    t_m = t

    t_res = []

    for curr_time in times:
        # цикл подсчета значений функции T
        t_m_plus_1 = simple_iteration_on_layer(t_m, curr_time, data, ops)

        t_res.append(t_m_plus_1)

        t_m = t_m_plus_1

    return np.array(x), np.array(times), np.array(t_res)


def get_optimal_h(data: Grid, ops: TaskOps):
    """
    Метод для получения оптимального шага по координате
    """
    print(f"[+] вызвал get_optimal_h")
    h = 0.2  # начальный шаг по координате

    count = 0
    while True:

        data.h = h
        x_h, times_h, t_res_h = simple_iteration(data, ops)
        t_h_0 = dict(zip(x_h, t_res_h[len(times_h) // 2]))

        data.h = h / 2
        x_h_half_2, times_h_half_2, t_res_h_half_2 = simple_iteration(data, ops)
        t_h_half_2_0 = dict(zip(x_h_half_2, t_res_h_half_2[len(times_h_half_2) // 2]))

        cnt = 0

        for x in t_h_0.keys():
            error = abs((t_h_0[x] - t_h_half_2_0[x]) / t_h_half_2_0[x])

            if error < EPS:
                cnt += 1

        if cnt == len(x_h):
            break

        h /= 2

        print(f"итерация №{count + 1}")
        count += 1

    return h


def get_optimal_tau(data: Grid, ops: TaskOps):
    """
    Метод для получения оптимального шага по времени
    """
    print(f"[+] вызвал get_optimal_tau")
    tau = 5  # начальный шаг по координате

    count = 0
    while True:

        data.tau = tau
        x_h, times_h, t_res_h = simple_iteration(data, ops)
        res = []
        for row in t_res_h:
            res.append(row[len(x_h) // 2])
        t_h_0 = dict(zip(times_h, res))

        data.tau = tau / 2
        x_h_half_2, times_h_half_2, t_res_h_half_2 = simple_iteration(data, ops)
        res = []
        for row in t_res_h_half_2:
            res.append(row[len(x_h_half_2) // 2])
        t_h_half_2_0 = dict(zip(times_h_half_2, res))

        cnt = 0
        for x in t_h_0.keys():
            error = abs((t_h_0[x] - t_h_half_2_0[x]) / t_h_half_2_0[x])

            if error < EPS:
                cnt += 1

        if cnt == len(times_h):
            break

        tau /= 2

        print(f"итерация №{count + 1}")
        count += 1

    return tau


def task2_f_max_t_max_by_x(data: Grid, ops: TaskOps):
    """
    2-й пункт лабы, разбил функцию на две (срез по координате)
    """
    print(f"[+] вызвал task2_f_max_t_max_by_x")
    f_max_list = [60, 50, 40, 30, 20, 10, 1]
    t_max_list = [70, 60, 50, 40, 30, 20, 10, 1]

    plt.figure(figsize=(14, 9))

    cnt = 0
    for i, f_max in enumerate(f_max_list):
        for j, t_max in enumerate(t_max_list):
            plt.subplot(len(f_max_list), len(t_max_list), i * len(t_max_list) + j + 1)

            ops.f_max = f_max
            ops.t_max = t_max
            x, t, t_res = simple_iteration(data, ops)

            # список номеров некоторых узлов сетки по координате для анализа
            list_ind_x = [0, len(t_res[0]) // 4, len(t_res[0]) // 2, len(t_res[0]) - 1]

            # цикл по некоторым узлам сетки
            for ind_x in list_ind_x:
                curr_t = [t_m[ind_x] for t_m in t_res]
                plt.xlabel("t, c")
                plt.ylabel("T(x, t)")
                plt.ylim((300, 700))
                plt.grid()
                plt.plot(t, curr_t, label=f"F_max={f_max} t_max={t_max} x={x[ind_x]}")
            plt.legend()

            print(f"итерация №{cnt + 1}")
            cnt += 1

    plt.savefig(f"../data/F_max_t_max_by_x.png")


def task2_f_max_t_max_by_t(data: Grid, ops: TaskOps):
    """
    2-й пункт лабы, разбил функцию на две (срез по времени)
    """
    print(f"[+] вызвал task2_f_max_t_max_by_t")
    f_max_list = [40, 50, 60]
    t_max_list = [50, 60, 70]

    plt.figure(figsize=(14, 9))

    cnt = 0
    for i, f_max in enumerate(f_max_list):
        for j, t_max in enumerate(t_max_list):
            plt.subplot(len(f_max_list), len(t_max_list), i * len(t_max_list) + j + 1)

            ops.f_max = f_max
            ops.t_max = t_max
            x, t, t_res = simple_iteration(data, ops)

            # список номеров узлов сетки по времени для анализа
            list_ind_t = [0, len(t_res) // 4, len(t_res) // 2, len(t_res) - 1]

            for ind_t in list_ind_t:
                curr_t = t_res[ind_t]
                plt.xlabel("x, cm")
                plt.ylabel("T(x, t)")
                plt.ylim((300, 750))
                plt.grid()
                plt.plot(x, curr_t, label=f"F_max={f_max} t_max={t_max} t={t[ind_t]}")
            plt.legend()

            print(f"итерация №{cnt + 1}")
            cnt += 1

    plt.savefig(f"../data/F_max_t_max_by_t.png")


def get_optimal_steps_by_f_max_t_max(data: Grid, ops: TaskOps):
    """
    Функция находит оптимальные шаги для различных F_max и t_max
    """
    print(f"[+] вызвал task2_f_max_t_max_by_t")
    table_size = 101
    file = open("../data/optimal_steps.txt", "w", encoding="utf-8")

    file.write("-" * table_size + "\n")
    file.write(f'| {"F_max": ^22} | {"t_max": ^22} | {"optimal h": ^22} | {"optimal tau": ^22} |\n')
    file.write("-" * table_size + "\n")

    f_max_list = [60, 50, 40, 30, 20, 10, 1]
    t_max_list = [70, 60, 50, 40, 30, 20, 10, 1]

    cnt = 0

    for f_max in f_max_list:
        for t_max in t_max_list:
            ops.f_max = f_max
            ops.t_max = t_max

            opt_h = get_optimal_h(data, copy(ops))
            opt_tau = get_optimal_tau(data, copy(ops))

            file.write(f'| {f_max: ^22} | {t_max: ^22} | {opt_h: ^22} | {opt_tau: ^22} |\n')

            print(f"итерация №{cnt + 1}")
            cnt += 1

    file.write("-" * table_size)

    file.close()


def task2_integral(data: Grid, ops: TaskOps):
    """
    Реализация вычисления интеграла во 2-м пункте методом трапеций
    (ссылка: https://ru.wikipedia.org/wiki/Метод_трапеций)
    """
    x, t, t_res = simple_iteration(data, ops)  # получили решение
    ind_t_m = -1  # получаем индекс времени для t_m

    eps = 1e-2  # другая своя точность

    t0, r = ops.t0, ops.r
    a, b, h = data.a, data.b, data.h

    # F0 и FN (формулы из краевых условий)
    f_0_value = - alpha(x[0], ops) * (t_res[-1][0] - t0)
    f_n_value = alpha(x[-1], ops) * (t_res[-1][-1] - t0)

    upper_integral = 0

    for i in range(0, len(x) - 1):
        first = alpha(x[i], ops) * (t_res[ind_t_m][i] - t0)
        second = alpha(x[i + 1], ops) * (t_res[ind_t_m][i] - t0)

        upper_integral += 0.5 * (first + second) * h

    lower_integral = 0

    for i in range(0, len(x) - 1):
        first = k(t_res[ind_t_m][i], ops) * np.exp(-k(t_res[ind_t_m][i], ops) * x[i])
        second = k(t_res[ind_t_m][i + 1], ops) * np.exp(-k(t_res[ind_t_m][i + 1], ops) * x[i + 1])

        lower_integral += 0.5 * (first + second) * h

    numerator = -f_0_value + f_n_value + (2 / r) * upper_integral  # числитель дроби
    denominator = f0(t[-1], ops) * lower_integral  # знаменатель дроби

    accuracy = abs(numerator / denominator - 1)
    print(f"accuracy = {accuracy}")

    if accuracy <= eps:
        print(f"все классно, мощность сбалансирована!")
    else:
        print(f"мощность не сбалансирована!")


def task3_a2_b2(data: Grid, ops: TaskOps):
    """
    3-й пункт лабы, изменение параметров a2 и b2 (срезы по координате)
    """
    print(f"[+] вызвал task3_a2_b2")
    # 2 значения -- по условию
    a2_list = [1, 2.049, 5]
    b2_list = [0.563e-3, 0.6e-2]

    plt.figure(figsize=(14, 9))

    cnt = 0
    for i, a2 in enumerate(a2_list):
        for j, b2 in enumerate(b2_list):
            plt.subplot(len(a2_list), len(b2_list), i * len(b2_list) + j + 1)

            ops.a2 = a2
            ops.b2 = b2
            x, t, t_res = simple_iteration(data, ops)

            t_0 = [t_m[0] for t_m in t_res]

            plt.plot(t, t_0, label=f"a2={a2} b2={b2}")
            plt.grid()
            plt.legend()

            print(f"итерация №{cnt + 1}")
            cnt += 1

    plt.savefig(f"../data/a2_b2_by_x.png")


def main() -> None:
    """
    Главная функция
    """
    ops = TaskOps()

    a, b = 0, ops.l  # диапазон значений координаты
    n = 100
    h = (b - a) / n

    t_max = 100
    time0, timem = 0, t_max  # диапазон значений времени
    m = 15000
    tau = (timem - time0) / m

    print(f"tau = {tau}, h = {h}")

    data = Grid(a, b, n, h, time0, timem, m, tau)

    """Задание №1"""

    # x, t, t_res = simple_iteration(data, ops)
    #
    # X, T = np.meshgrid(x, t)
    #
    # # Построение графика
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.plot_surface(X, T, t_res, cmap='viridis')
    #
    # # Настройка подписей осей
    # ax.set_xlabel('x')
    # ax.set_ylabel('t')
    # ax.set_zlabel('T(x, t)')
    # ax.set_title('Температурное поле')
    #
    # plt.show()

    """Задание №2"""

    # get_optimal_steps_by_f_max_t_max(data, copy(ops))

    # opt_h = get_optimal_h(data, copy(ops))  # 0.0025.
    # print(f"opt_h = {opt_h}")
    # opt_tau = get_optimal_tau(data, copy(ops))  # 1.25
    # print(f"opt_tau = {opt_tau}")
    #
    # data.h, data.tau = opt_h, opt_tau
    #
    # task2_integral(data, copy(ops))

    """Задание №3"""

    # task3_a2_b2(data, copy(ops))

    """Задание №4"""

    # Создание нового окна для двумерных графиков
    fig2, axes = plt.subplots(2, 3, figsize=(13, 10))

    t_f0 = np.arange(time0, t_max + tau, tau)

    res = []
    for curr_t in t_f0:
        res.append(f0(curr_t, copy(ops)))

    # Построение двумерных графиков
    axes[0, 0].plot(t_f0, res, 'g', label="F0(t)")
    axes[0, 0].set_title('График F0')
    axes[0, 0].set_xlabel('t')
    axes[0, 0].set_ylabel('F0')
    axes[0, 0].legend()
    axes[0, 0].grid()

    x, t, t_res = simple_iteration(data, copy(ops))

    res = []
    for t_m in t_res:
        res.append(t_m[0])

    # Построение двумерных графиков
    axes[0, 1].plot(t, res, 'g', label=f"T(0, t)")
    axes[0, 1].set_title('График T')
    axes[0, 1].set_xlabel('t')
    axes[0, 1].set_ylabel('T(0, t)')
    axes[0, 1].legend()
    axes[0, 1].grid()

    # res, a2_list = get_data_graph_task_3(data, ops)
    #
    # for i, res_i in enumerate(res):
    #     axes[0, 1].plot(t, res_i[:-1], label=f"T(0, t), a2 = {a2_list[i]}")
    # axes[0, 1].set_title('График T(0, t)')
    # axes[0, 1].set_xlabel('t')
    # axes[0, 1].set_ylabel('T(0, t)')
    # axes[0, 1].legend()
    # axes[0, 1].grid()
    # #
    # res, b2_list = get_data_graph_task_3_2(data, ops)
    #
    # for i, res_i in enumerate(res):
    #     axes[0, 2].plot(t, res_i[:-1], label=f"T(0, t), b2 = {b2_list[i]}")
    # axes[0, 2].set_title('График T(0, t)')
    # axes[0, 2].set_xlabel('t')
    # axes[0, 2].set_ylabel('T(0, t)')
    # axes[0, 2].legend()
    # axes[0, 2].grid()

    # a, b = 0, 10  # диапазон значений координаты
    # n = 1000
    # h = (b - a) / n
    # time0, timem = 0, ops.t_max  # диапазон значений времени
    # m = ops.t_max
    # tau = (timem - time0) / m
    #
    # data = Grid(a, b, n, h, time0, timem, m, tau)
    #
    # t_res = np.array(simple_iteration(data, ops))[:-1]

    # for i, res_i in enumerate(t_res):
    #     axes[1, 0].plot(x, res_i, label=f"T(x, t), t = {t[i]}")
    # axes[1, 0].set_title('График T(x, t)')
    # axes[1, 0].set_xlabel('t')
    # axes[1, 0].set_ylabel('T(x, t)')
    # axes[1, 0].legend()
    # axes[1, 0].grid()

    # Показать график
    plt.show()


if __name__ == '__main__':
    main()
