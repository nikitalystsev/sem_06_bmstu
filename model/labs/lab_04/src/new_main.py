import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
import scipy

DEBUG = False
DEBUG2 = False


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
    t0: int | float = 300  # температура обдувающего воздуха
    r: int | float = 0.5  # радиус стержня

    alpha_0: int | float = 0.05  # ок в x = 0
    alpha_n: int | float = 0.01  # ок в x = l

    d: int | float = 0.01 * l / (-0.04)  # ок
    c: int | float = -0.05 * d  # ок

    # для отладки принять
    f_max: int | float = 50  # амплитуда импульса (определяет крутизну фронтов)
    t_max: int | float = 60  # время (определяет длительность импульса)


# Простая аппроксимация
# def func_plus_half(func, n, m=None):
#     if m:
#         return (func(n, m) + func(n + 1, m)) / 2
#     else:
#         return (func(n) + func(n + 1)) / 2


# def func_minus_half(func, n, m=None):
#     if m:
#         return (func(n, m) + func(n - 1, m)) / 2
#     else:
#         return (func(n) + func(n - 1)) / 2

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

    return (f_max / t_max) * time * np.exp(-((time / t_max) - 1))
    # return (f_max / t_max) * 20 * np.exp(-((20 / t_max) - 1))
    # return 20


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

    # if x > 0:
    #     return (2 * t0 / r) * alpha(x, ops)

    return k(t, ops) * f0(time, ops) * np.exp(-k(t, ops) * x) + (2 * t0 / r) * alpha(x, ops)


class Solver:
    # a2 = 2.049
    # b2 = 0.563e-3
    def __init__(self, xmin=0, xmax=10, h=0.01, tmin=0, tau=0.5, EPS=None, Fmax=50, tmax=60, a2=2.049, b2=0.563e-3,
                 use_constant_F0t=None, v=None):
        self.xmin = xmin
        self.xmax = xmax
        self.h = h
        self.tmin = tmin
        self.tau = tau
        if EPS:
            self.EPS = EPS
        else:
            self.EPS = self.h / 100
        self.Fmax = Fmax
        self.tmax = tmax
        self.l = xmax - xmin
        self.a2 = a2
        self.b2 = b2
        self.use_constant_F0t = use_constant_F0t
        self.v = v
        if v:
            self.period_by_m = round(1 / (v['v'] * tau))
            if self.period_by_m <= 1:
                self.period_by_m = 1
                print('WARNING, it is not periodical')

        if v and use_constant_F0t:
            raise ValueError('v and use_constant_F0t simultaneously')

    # коэффициент теплопроводимости материала стержня
    def lambda_T(self, n, m):
        return a1 * (b1 + c1 * pow(self.T[m][n], m1))

    def kappa_T(self, n, m):
        return self.lambda_T(n, m)

    # коэффициент теплоемкости материала стержня
    def c_T(self, n, m):
        return self.a2 + self.b2 * pow(self.T[m][n], m2) - c2 / (self.T[m][n] ** 2)

    # коэффициент оптического поглощения материала стержня
    def k_T(self, n, m):
        return k0 * pow(self.T[m][n] / 300, 2)

    def exp_Tx(self, n, m):
        return exp(-self.k_T(n, m) * self.x_array[n])

    # коэффициент теплоотдачи при обдуве
    def alpha_x(self, n):
        alpha0 = 0.05
        alphaN = 0.01
        d_for_alpha = (alphaN * self.l) / (alphaN - alpha0)
        c_for_alpha = - alpha0 * d_for_alpha
        return c_for_alpha / (self.x_array[n] - d_for_alpha)

    # !?
    # импульс излучения

    def F0_t(self, m):
        if self.use_constant_F0t:
            if m < self.use_constant_F0t['stop_hitting']:
                return self.Fmax * self.use_constant_F0t['constantF0t_t'] * exp(
                    -(self.use_constant_F0t['constantF0t_t'] / self.tmax - 1)) / self.tmax
            else:
                return 0

        if self.v and (m % self.period_by_m) != 1:
            return 0

        # if self.v < 1:
        #     raise ValueError('v<1')
        # # Импульсы следуют один за другим с заданной частотой v
        # # (частота определяется количеством импульсов в 1 секунду).
        # here_eps = 1e-6
        # imp_each_part = 1 / self.v if self.v != 1 else 0
        # float_part_of_cur_time = t % 1
        # for i in range(self.v): # 1/3 2/3 3/3
        #     if abs(float_part_of_cur_time - imp_each_part * i) < here_eps:
        #         #print(f'!!!!!! for m={m}')
        #         return self.Fmax * t * exp(-(t / self.tmax - 1)) / self.tmax
        # # значит  время неподходящее
        # return 0

        t = self.tmin + self.tau * m
        return self.Fmax * t * exp(-(t / self.tmax - 1)) / self.tmax

    def solve(self):
        self.x_array = list(np.arange(self.xmin, self.xmax + self.EPS, self.h))
        self.N = len(self.x_array)

        self.T = []
        self.t_array = []
        self.T.append([T0] * self.N)
        self.t_array.append(0)

        m = 1
        while True:
            if m % 100 == 0:
                print('m (by t) =', m)
            if DEBUG:
                print(f"\n\nStart counting for time {m} ({self.t_array[-1] + self.tau})")
            # print(f"\n\nStart counting for time {m} ({self.t_array[-1] + self.tau})")
            # начальное приближение - сошедшееся с предыдущего шага
            self.T.append(self.T[-1])

            iterations_counter = 0
            while True:
                iterations_counter += 1
                if DEBUG:
                    print(f"Iteration {iterations_counter}")
                # if iterations_counter > 1:
                #     print('wow, iteration > 1', iterations_counter)
                T_m_prev_iteration = self.T[-1]
                T_m_cur_iteration = self.count_T_array_for_time_m(m)
                self.T[-1] = T_m_cur_iteration
                if self.stop_iterating(T_m_prev_iteration, T_m_cur_iteration):
                    break

            if self.stop_timing():
                break

            m += 1
            self.t_array.append(self.t_array[-1] + self.tau)
        self.t_array.append(self.t_array[-1] + self.tau)
        return self.get_results()

    def get_results(self):
        return self.T, self.t_array

    def check_T(self):
        for Tm in self.T:
            for T_cur in Tm:
                if T_cur > 2000:
                    print('\n\n\n\n\n\n!!!!!!!!!!T>2000\n\n\n\n\n\n\n')

    def count_boundary_conditions(self, m):
        # считаем для того же m, но с предыдущей итерации
        # изначально ошиблась, думая,что с предыдущего времени
        m += 1

        # N должна быть просто последний элемент массива
        self.N -= 1

        K0 = (self.h * func_plus_half(self.c_T, 0, m - 1) / 8 +
              self.h * self.c_T(0, m - 1) / 4 +
              self.tau * func_plus_half(self.kappa_T, 0, m - 1) / self.h +
              self.h * self.tau * func_plus_half(self.alpha_x, 0) / (4 * R) +
              self.h * self.tau * self.alpha_x(0) / (2 * R) +
              self.alpha_x(0) * self.tau)

        M0 = (self.h * func_plus_half(self.c_T, 0, m - 1) / 8 -
              self.tau * func_plus_half(self.kappa_T, 0, m - 1) / self.h +
              self.h * self.tau * func_plus_half(self.alpha_x, 0) / (4 * R))

        # p1 = self.h * func_plus_half(self.c_T, 0, m - 1) * (self.T[m - 1][0] + self.T[m - 1][1]) / 8
        # p2 = self.h * self.c_T(0, m - 1) * self.T[m - 1][0] / 4
        # p3 =  self.alpha_x(0) * self.tau * T0
        # p4 = (self.h * self.tau / 4 ) * (2 * T0 * (func_plus_half(self.alpha_x, 0) + self.alpha_x(0)) / R)
        # p5 = (self.h * self.tau / 4 ) * self.F0_t(m - 1) * self.k_T(0, m - 1) * self.exp_Tx(0, m - 1)
        # p6 = (self.h * self.tau / 4 ) * self.F0_t(m - 1) * func_plus_half(self.k_T, 0, m - 1) * func_plus_half(self.exp_Tx, 0, m - 1)
        correct_exp_one_half = exp(-func_plus_half(self.k_T, 0, m - 1) * (self.x_array[0] + self.x_array[1]) / 2)
        P0 = (self.h * func_plus_half(self.c_T, 0, m - 1) * (self.T[m - 1][0] + self.T[m - 1][1]) / 8 +
              self.h * self.c_T(0, m - 1) * self.T[m - 1][0] / 4 +
              self.alpha_x(0) * self.tau * T0 +
              self.h * self.tau * (
                      self.F0_t(m - 1) * (self.k_T(0, m - 1) * self.exp_Tx(0, m - 1) + func_plus_half(self.k_T, 0,
                                                                                                      m - 1) * correct_exp_one_half) +
                      2 * T0 * (func_plus_half(self.alpha_x, 0) + self.alpha_x(0)) / R
              ) / 4)

        KN = (self.h * func_minus_half(self.c_T, self.N, m - 1) / 8 +
              self.h * self.c_T(self.N, m - 1) / 4 +
              self.tau * func_minus_half(self.kappa_T, self.N, m - 1) / self.h +
              self.h * self.tau * func_minus_half(self.alpha_x, self.N) / (4 * R) +
              self.h * self.tau * self.alpha_x(self.N) / (2 * R) +
              self.alpha_x(self.N) * self.tau)

        MN = (self.h * func_minus_half(self.c_T, self.N, m - 1) / 8 -
              self.tau * func_minus_half(self.kappa_T, self.N, m - 1) / self.h +
              self.h * self.tau * func_minus_half(self.alpha_x, self.N) / (4 * R))

        correct_exp_one_half = exp(
            -func_minus_half(self.k_T, self.N, m - 1) * (self.x_array[self.N] + self.x_array[self.N - 1]) / 2)
        func_minus_half(self.exp_Tx, self.N, m - 1)
        PN = (self.h * func_minus_half(self.c_T, self.N, m - 1) * (
                self.T[m - 1][self.N] + self.T[m - 1][self.N - 1]) / 8 +
              self.h * self.c_T(self.N, m - 1) * self.T[m - 1][self.N] / 4 +
              self.alpha_x(self.N) * self.tau * T0 +
              self.h * self.tau * (
                      self.F0_t(m - 1) * (
                      self.k_T(self.N, m - 1) * self.exp_Tx(self.N, m - 1) + func_minus_half(self.k_T, self.N,
                                                                                             m - 1) * correct_exp_one_half) +
                      2 * T0 * (func_minus_half(self.alpha_x, self.N) + self.alpha_x(self.N)) / R
              ) / 4)

        self.N += 1

        # MN, KN = KN, MN
        # M0, K0 = K0, M0
        return {"K0": K0, "M0": M0, "P0": P0,
                "KN": KN, "MN": MN, "PN": PN, }

    def count_coeffs(self, n, m):
        # считаем для того же m, но с предыдущей итерации
        # изначально ошиблась, думая,что с предыдущего времени
        m += 1

        A = self.tau * func_minus_half(self.kappa_T, n, m - 1) / self.h
        D = self.tau * func_plus_half(self.kappa_T, n, m - 1) / self.h
        B = self.h * self.c_T(n, m - 1) + A + D + 2 * self.h * self.tau * self.alpha_x(n) / R
        sum1 = self.h * self.c_T(n, m - 1) * self.T[m - 1][n]
        sum2 = self.h * self.tau * self.k_T(n, m - 1) * self.F0_t(m - 1) * self.exp_Tx(n, m - 1)
        sum3 = 2 * self.h * self.tau * T0 * self.alpha_x(n) / R
        F = self.h * self.c_T(n, m - 1) * self.T[m - 1][n] + \
            self.h * self.tau * self.k_T(n, m - 1) * self.F0_t(m - 1) * self.exp_Tx(n, m - 1) + \
            2 * self.h * self.tau * T0 * self.alpha_x(n) / R
        return {"A": A, "B": B, "D": D, "F": F}

    def count_T_array_for_time_m(self, m):
        boundary_conditions = self.count_boundary_conditions(m)

        # Прямой ход
        ksi_array = [-boundary_conditions['M0'] / boundary_conditions["K0"]]
        eta_array = [boundary_conditions['P0'] / boundary_conditions["K0"]]

        # x = self.h
        # n = 1
        if DEBUG2:
            print('\n\n\nm=', m)
            print(boundary_conditions)
        for n in range(1, self.N - 1):
            if DEBUG2:
                print(f"n={n}", end=' ')
            # while (x + self.h < l):
            cur_coeffs = self.count_coeffs(n, m)
            if DEBUG2:
                print(cur_coeffs, end=' ')
            ksi_array.append(cur_coeffs["D"] / (cur_coeffs["B"] - cur_coeffs["A"] * ksi_array[n - 1]))
            eta_array.append((cur_coeffs["F"] + cur_coeffs["A"] * eta_array[n - 1]) /
                             (cur_coeffs["B"] - cur_coeffs["A"] * ksi_array[n - 1]))
            if DEBUG2:
                print(f"ksi={ksi_array[-1]}, eta={eta_array[-1]}")
            # n += 1
            # x += self.h

        # Обратный ход
        T_cur_array = [0] * self.N
        T_cur_array[-1] = ((boundary_conditions['PN'] - boundary_conditions['MN'] * eta_array[-1]) /
                           (boundary_conditions['KN'] + boundary_conditions['MN'] * ksi_array[-1]))

        for i in range(self.N - 2, -1, -1):
            T_cur_array[i] = ksi_array[i] * T_cur_array[i + 1] + eta_array[i]

        return T_cur_array

    def stop_timing(self):
        if self.use_constant_F0t:
            return len(self.T) * self.tau > self.use_constant_F0t['stop_timing']
        if self.v:
            return len(self.T) * self.tau > self.v['stop_timing']
        T_array_prev, T_array_new = self.T[-2], self.T[-1]
        for T_prev, T_cur in zip(T_array_prev, T_array_new):
            if abs((T_prev - T_cur) / T_cur) > 1e-4:
                return False
        return True

    def stop_iterating(self, T_array_prev, T_array_new):
        if len(T_array_prev) != self.N or len(T_array_new) != self.N:
            raise ValueError('NNNN')
        differences = [abs((T_array_new[n] - T_array_prev[n]) / T_array_new[n]) for n in range(self.N)]
        max_difference = max(differences)
        return max_difference < 1

    def print_results(self, add_str=''):
        columns = [f'{x}' for x in range(int(self.xmax))]
        table = pd.DataFrame(index=self.t_array)
        for i in range(0, len(self.x_array), int(len(self.x_array) // self.xmax)):
            table[f'{self.x_array[i]}'] = [Tm[i] for Tm in self.T]

        # table = table.set_index('z')

        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_colwidth', None)
        pd.options.display.float_format = '{:,.9e}'.format

        # table.to_excel(f'{add_str}result.xls')

    def show_results(self, add_str=''):
        M = len(self.T)  # обрезаем неинтересную часть графика

        # Трехмерный
        x, y = np.mgrid[0:self.t_array[-1] + self.EPS:self.tau, 0:self.xmax + self.EPS:self.h]
        z = np.array([np.array(T_m) for T_m in self.T])

        fig_3d = plt.figure()
        xyz = fig_3d.add_subplot(111, projection='3d')
        xyz.plot_surface(x, y, z, cmap='Oranges')
        plt.xlabel("t, c")
        plt.ylabel("x, см")
        fig_3d.show()
        plt.savefig(f'{add_str}3d.png')

        plt.show()
        # # Проекции
        # fig, (first_graph, second_graph) = plt.subplots(
        #     nrows=1, ncols=2,
        #     figsize=(8, 4))
        #
        # # Первая cm - K
        # step_by_time = int(len(self.T) / 10) + 1
        # for T_m in self.T[len(self.T) - 1:0:-step_by_time]:
        #     first_graph.plot(self.x_array, T_m, label=f't={self.t_array[self.T.index(T_m)]}')
        # first_graph.set_xlabel("x, cm")
        # first_graph.set_ylabel("T, K")
        # plt.legend()
        # first_graph.grid()
        #
        # # Вторая sec - K
        # step_by_cm = int(len(self.x_array) / 10)
        # for i in range(0, len(self.x_array), step_by_cm):
        #     line = [T_m[i] for T_m in self.T]
        #     second_graph.plot(self.t_array, line, label=f'{self.x_array[i]}')
        #
        # second_graph.set_xlabel("t, sec")
        # second_graph.set_ylabel("T, K")
        # second_graph.grid()
        # plt.legend()
        # fig.show()
        # plt.savefig(f'{add_str}2d.png')
        # print()

    def check_steps_ok(self):
        eps = 1e-2
        M = len(self.T)
        F0_value = self.alpha_x(0) * (T0 - self.T[-1][0])
        FN_value = self.alpha_x(self.N - 1) * (self.T[-1][-1] - T0)

        # средние
        upper_integral = 0
        for i in range(1, self.N):
            sum1 = self.alpha_x(i) * (self.T[-1][i] - T0)
            sum2 = self.alpha_x(i - 1) * (self.T[-1][i - 1] - T0)
            upper_integral += (sum1 + sum2)
            # upper_integral += func_minus_half(self.alpha_x, i) * (((self.T[-1][i] + self.T[-1][i-1]) / 2) - T0)
        upper_integral *= (self.h / R)
        # upper_integral_2 = scipy.integrate.trapezoid

        F0t = self.F0_t(M - 1)

        lower_integral = 0
        for i in range(1, self.N):
            sum1 = self.k_T(i, M - 1) * self.exp_Tx(i, M - 1)
            sum2 = self.k_T(i - 1, M - 1) * self.exp_Tx(i - 1, M - 1)
            lower_integral += (sum1 + sum2)
            # lower_integral += func_minus_half(self.k_T, i, M - 1) * func_minus_half(self.exp_Tx, i, M-1) * self.h

        chisl = -F0_value + FN_value + upper_integral
        znam = F0t * lower_integral

        counted = abs((chisl / znam) - 1)
        if znam < 1e-6:
            print()
        #  print('counted', counted)
        return counted <= eps, counted


def study2_steps():
    # tau=0.5, h = 0.01
    h_array = [1, 10, 100, 1000]  # 1/h
    tau_array = [1, 0.5, 0.1]
    x_array = list(np.arange(0, 10 + 1e-4, 1))
    results = pd.DataFrame(
        columns=['h', 'tau', 'h * tau', 'balanced', 'M', 'counted_dif', ] + [f'x={x}' for x in x_array])

    for h in h_array:
        for tau in tau_array:
            solver = Solver(h=1 / h, tau=tau)
            solver.solve()
            T, t_array = solver.get_results()
            T_last = T[-1]
            balanced, counted = solver.check_steps_ok()
            row_pd = {'h': 1 / h, 'tau': tau, 'h * tau': tau / h, 'balanced': balanced, 'M': len(t_array),
                      'counted_dif': counted}
            print(row_pd)
            row_pd.update({f'x={x_array[i]}': T_last[i * h] for i in range(len(x_array))})
            results = results.append(row_pd, ignore_index=True)
    results = results.sort_values(by=['h * tau', 'tau', 'h'], axis=0, ascending=False)
    try:
        results.to_excel('study_steps.xls')
    except:
        results.to_excel('study_steps2.xls')


# График зависимости температуры T(0,t) от a2, b2
# С ростом теплоемкости (этих коэффициентов) темп нарастания температуры снижается
# коэффициент теплоемкости материала стержня
# def c_T(self, n, m):
#       return self.a2 + self.b2 * pow(self.T[m][n], m2) - c2 / (self.T[m][n] ** 2)
def study3_ab():
    print('research ab')
    # 2 значения -- по условию
    a2_array = [1, 2.049, 5]
    b2_array = [0.563e-3, 0.6e-2]
    fig = plt.figure(figsize=(14, 9))

    for i, a2 in enumerate(a2_array):
        for j, b2 in enumerate(b2_array):
            title = f"a2={a2} b2={b2}"
            plt.subplot(len(a2_array), len(b2_array), i * len(b2_array) + j + 1)

            solver = Solver(a2=a2, b2=b2)
            solver.solve()
            T, t_array = solver.get_results()

            T_0t = [T_m[0] for T_m in T]
            plt.xticks(t_array[::len(t_array) // 10])
            plt.plot(t_array, T_0t, label=title)
            plt.grid()
            plt.legend()

            print(f'a2={a2}, b2={b2}')

    plt.savefig(f"a2b2.png")
    plt.show()


# в 1 бьет
def study4_impuls():
    in_row = 3
    stop_timing = 600
    print('research impuls')
    v_array = [0.01, 0.05, 0.1, 1, 3, 5]  # больше низя
    fig = plt.figure(figsize=(14, 9))

    for i, v in enumerate(v_array):
        title = f"v={v}"
        print(title)
        plt.subplot(ceil(len(v_array) / in_row), in_row, i + 1)

        solver = Solver(v={'v': v, 'stop_timing': stop_timing}, h=0.1, tau=0.1)
        solver.solve()
        T, t_array = solver.get_results()
        print(len(T))

        T_0t = [T_m[0] for T_m in T]
        plt.xticks(list(range(0, stop_timing, int(stop_timing / 10))))
        plt.plot(t_array, T_0t, label=title)
        plt.legend()

    plt.savefig(f"v.png")
    plt.show()


# Рассмотреть влияние на получаемые результаты амплитуды импульса Fmax и времени maxt
# (определяют крутизну фронтов и длительность импульса).
def study5_Ftmax():
    # сильнее нагревается
    def study_cm():
        q = 0
        fig = plt.figure(figsize=(14, 9))
        for i, Fmax in enumerate(Fmax_array):
            for j, tmax in enumerate(tmax_array):
                title = f"Fmax={Fmax} tmax={tmax}"
                plt.subplot(len(Fmax_array), len(tmax_array), i * len(tmax_array) + j + 1)
                q += 1

                solver = Solver(Fmax=Fmax, tmax=tmax)
                solver.solve()
                T, t_array = solver.get_results()

                for cm in [0, int(len(T[0]) / 4), int(len(T[0]) / 2), len(T[0]) - 1]:
                    T_t = [T_m[cm] for T_m in T]
                    plt.xticks(list(range(0, 100, 10)))
                    plt.xlabel("t, c")
                    plt.ylim((300, 700))
                    plt.grid()
                    plt.plot(t_array, T_t, label=title + f'cm={solver.x_array[cm]}')
                plt.legend()

                print(f'Fmax={Fmax}, tmax={tmax}')
        plt.savefig(f"Fmaxtmax_cm.png")
        plt.show()

    # позже выходит на плато
    def study_t():
        q = 0
        fig = plt.figure(figsize=(14, 9))
        for i, Fmax in enumerate(Fmax_array):
            for j, tmax in enumerate(tmax_array):
                title = f"Fmax={Fmax} tmax={tmax}"
                plt.subplot(len(Fmax_array), len(tmax_array), i * len(tmax_array) + j + 1)
                q += 1

                solver = Solver(Fmax=Fmax, tmax=tmax)
                solver.solve()
                T, t_array = solver.get_results()

                for t in [0, int(len(T) / 4), int(len(T) / 2), len(T) - 1]:
                    T_t = T[t]
                    plt.xticks(list(range(0, 10, 1)))
                    plt.xlabel("x, cm")
                    plt.ylim((300, 750))
                    plt.grid()
                    plt.plot(solver.x_array, T_t, label=title + f't={solver.t_array[t]}')
                plt.legend()

                print(f'Fmax={Fmax}, tmax={tmax}')
        plt.savefig(f"Fmaxtmax_t.png")
        plt.show()

    # Fmax = 50
    # tmax = 60
    Fmax_array = [40, 50, 60]
    tmax_array = [50, 60, 70]
    study_t()
    study_cm()


# Если в настоящей работе задать поток постоянным, т.е. F0(t) =const, то будет
# происходить формирование температурного поля от начальной температуры T0
# до некоторого установившегося (стационарного) распределения T(x,t)
# Это поле в дальнейшем с течением времени меняться не будет. Это полезный факт для тестирования программы.
# Если после разогрева стержня положить поток F(t)=0, то будет происходить
# остывание, пока температура не выровняется по всей длине и не станет равной T0
def test_with_constant_F0_t():
    # этот флаг выставляет константную F0_t(t=1) до 50 итерации по времени (должен выйти на константы)
    # далее считаем, что стержень нагрелся, и F0_t=0 (температура по всей длине должна стать 300
    # прекращаем все итерации на t=100,
    solver = Solver(use_constant_F0t={"constantF0t_t": 1, 'stop_timing': 600, 'stop_hitting': 800}, tau=0.5, h=0.01)
    solver.solve()
    solver.show_results(add_str='test_F0t_')
    solver.print_results(add_str='test_F0t_')


def main():
    # solver = Solver(tau=0.5, h=0.01, Fmax=200)
    # solver.solve()
    # solver.show_results()
    # solver.print_results()
    # print(solver.check_steps_ok())

    # SUPER OK
    test_with_constant_F0_t()

    # OK do
    # study2_steps()

    # OK
    # study3_ab()

    # study4_impuls()

    # OK
    # study5_Ftmax()


if __name__ == '__main__':
    main()
