import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from typing import Callable

from radiation_transfer_system import RadiationTransferSystem

EPS = 1e-4


class SolutionSystemByShootingMethod:
    """
    Класс для решения задачи второй лабораторной методом стрельбы
    """

    def __init__(self) -> None:
        """
        Инициализация атрибутов класса
        """
        # класс системы уравнений
        self.__system = RadiationTransferSystem()

        # 0 <= z <= 1
        self.__a = 0
        self.__b = 1

        self.__n = 10  # число узлов
        self.__h = (self.__b - self.__a) / self.__n  # шаг

        # ksi <= 1 и, наверное, больше нуля
        self.__ksi_a = 1e-2
        self.__ksi_b = 1

        self.__f_0 = 0

    def __runge_kutta_2(
            self,
            u_0: int | float,  # параметры - начальные условия задачи Коши
            f_0: int | float
    ):
        """
        Реализация метода Рунге Кутта 2-го порядка
        """
        is_k1 = True
        # is_k1 = False

        alpha = 1  # задаваемый параметр
        half_h = self.__h / 2

        z_res = np.arange(self.__a, self.__b + self.__h, self.__h)
        u_res = np.zeros(len(z_res))
        f_res = np.zeros(len(z_res))

        u_n = u_0
        f_n = f_0

        for i, z in enumerate(z_res):
            u_res[i] = u_n
            f_res[i] = f_n

            k1 = self.__system.der_u(z, f_n, is_k1=is_k1)
            q1 = self.__system.der_f(z, u_n, f_n, is_k1=is_k1)

            k2 = self.__system.der_u(z + half_h, f_n + half_h * q1, is_k1=is_k1)
            q2 = self.__system.der_f(z + half_h, u_n + half_h * k1, f_n + half_h * q1, is_k1=is_k1)

            u_n += self.__h * ((alpha - 1) * k1 + alpha * k2)
            f_n += self.__h * ((alpha - 1) * q1 + alpha * q2)

        return z_res, u_res, f_res

    def __runge_kutta_4(
            self,
            u_0: int | float,  # параметры - начальные условия задачи Коши
            f_0: int | float
    ):
        """
        Реализация метода Рунге Кутта 4-го порядка
        """
        is_k1 = True
        # is_k1 = False

        half_h = self.__h / 2

        z_res = np.arange(self.__a, self.__b + self.__h, self.__h)
        u_res = np.zeros(len(z_res))
        f_res = np.zeros(len(z_res))

        u_n = u_0
        f_n = f_0

        for i, z in enumerate(z_res):
            u_res[i] = u_n
            f_res[i] = f_n

            k1 = self.__system.der_u(z, f_n, is_k1=is_k1)
            q1 = self.__system.der_f(z, u_n, f_n, is_k1=is_k1)

            k2 = self.__system.der_u(z + half_h, f_n + half_h * q1, is_k1=is_k1)
            q2 = self.__system.der_f(z + half_h, u_n + half_h * k1, f_n + half_h * q1, is_k1=is_k1)

            k3 = self.__system.der_u(z + half_h, f_n + half_h * q2, is_k1=is_k1)
            q3 = self.__system.der_f(z + half_h, u_n + half_h * k2, f_n + half_h * q2, is_k1=is_k1)

            k4 = self.__system.der_u(z + self.__h, f_n + self.__h * q3, is_k1=is_k1)
            q4 = self.__system.der_f(z + self.__h, u_n + self.__h * k3, f_n + self.__h * q3, is_k1=is_k1)

            u_n += (self.__h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
            f_n += (self.__h / 6) * (q1 + 2 * q2 + 2 * q3 + q4)

        return z_res, u_res, f_res

    def __scipy_solve(
            self,
            u_0: int | float,  # параметры - начальные условия задачи Коши
            f_0: int | float
    ):
        """
        Метод для решения поставленной задачи с помощью мат. пакета
        """
        is_k1 = True

        # is_k1 = False

        def f(z, s):
            """
            Для передачи ее в мат. пакет
            """
            dudz = self.__system.der_u(z, s[1], is_k1=is_k1)
            dfdz = self.__system.der_f(z, s[0], s[1], is_k1=is_k1)

            return [dudz, dfdz]

        z_res = np.arange(self.__a, self.__b + self.__h, self.__h)
        s0 = [u_0, f_0]

        solution = solve_ivp(f, (self.__a, self.__b), s0, t_eval=z_res)

        return z_res, solution.y[0], solution.y[1]

    def __psi(self, u, f):
        """
        Функция правого краевого условия
        """

        return f - 0.393 * self.__system.c * u

    def __get_init_cond(self, curr_ksi, func_rk: Callable):
        """
        Метод для получения начальных условий при решении методом стрельбы
        """
        _, u, f = func_rk(curr_ksi * self.__system.u_p(0), self.__f_0)

        return self.__psi(u[-1], f[-1])

    def __get_solve_by_rk(self, func_rk: Callable):
        """
        Метод, реализующий общее методов Рунге-Кутты
        """
        ksi_start, ksi_end = self.__ksi_a, self.__ksi_b  # начальный интервал неопределенности
        ksi_curr = 0

        condition = True

        # реализация метода дихотомии для нахождения корня уравнения
        # psi(u(b, s), F(b, s)) = 0, где s - начальное значение в методе стрельбы
        while condition:
            ksi_curr = (ksi_start + ksi_end) / 2  # находим середину текущего интервала неопределенности

            f_ksi_start = self.__get_init_cond(ksi_start, func_rk)
            f_ksi_curr = self.__get_init_cond(ksi_curr, func_rk)
            f_ksi_end = self.__get_init_cond(ksi_end, func_rk)

            if f_ksi_start * f_ksi_curr < 0:
                ksi_end = ksi_curr
            if f_ksi_curr * f_ksi_end < 0:
                ksi_start = ksi_curr

            if abs((ksi_end - ksi_start) / ksi_curr) <= EPS:
                condition = False

        u_0 = ksi_curr * self.__system.u_p(0)

        z, u, f = func_rk(u_0=u_0, f_0=self.__f_0)

        return z, u, f, ksi_start, ksi_end

    def get_solve_by_rk_2(self):
        """
        Метод для получения решения системы методом Рунге-Кутты 2-го порядка точности
        """
        z, u, f, ksi_start, ksi_end = self.__get_solve_by_rk(self.__runge_kutta_2)

        return z, u, f, ksi_start, ksi_end

    def get_solve_by_rk_4(self):
        """
        Метод для получения решения системы методом Рунге-Кутты 4-го порядка точности
        """
        z, u, f, ksi_start, ksi_end = self.__get_solve_by_rk(self.__runge_kutta_4)

        return z, u, f, ksi_start, ksi_end

    def get_solve_by_scipy(self):
        """
        Метод для получения решения системы мат пакетом
        """
        z, u, f, ksi_start, ksi_end = self.__get_solve_by_rk(self.__scipy_solve)

        return z, u, f, ksi_start, ksi_end

    def print_solve(self, func_solve: Callable, filename: str):
        """
        Метод для получения решения
        """

        # z_rk2, u_rk2, f_rk2 = self.get_solve_by_rk_2()
        # z_rk4, u_rk4, f_rk4 = self.get_solve_by_rk_4()
        #
        # # Отключаем интерактивный режим
        # plt.ioff()
        #
        # fig, axs = plt.subplots(1, 2, figsize=(11, 7))
        #
        # # Первый график
        # axs[0].plot(z_rk2, u_rk2, label="Рунге-Кутта 2-го порядка")
        # axs[0].plot(z_rk4, u_rk4, label="Рунге-Кутта 4-го порядка")
        # axs[0].grid(True)
        # axs[0].set_title("u(z)")
        # axs[0].legend()
        #
        # # # Второй график
        # axs[1].plot(z_rk2, self.__system.u_p(z_rk2), label="РК 2-го порядка")
        # axs[1].plot(z_rk4, self.__system.u_p(z_rk4), label="РК 4-го порядка")
        # axs[1].set_title('u_p(z)')
        # axs[1].grid(True)
        # axs[1].legend()
        #
        # # Сохраняем графики в файл
        # fig.savefig(graph_path)
        #
        # # Включаем интерактивный режим обратно
        # plt.ion()

        z, u, f, ksi_start, ksi_end = func_solve()

        with open(f"../data/{filename}.txt", "w", encoding="utf-8") as file:
            file.write(f"ksi принадлежит интервалу ({ksi_start: <10.6f}, {ksi_end: 10.6f})\n")

            file.write("-" * 61 + "\n")
            file.write(f'| {"x": ^7} | {"u(z)": ^22} | {"F(z)": ^22} |\n')
            file.write("-" * 61 + "\n")

            for i in range(len(z)):
                file.write(f"| {z[i]: ^7.5f} | {u[i]: ^22.6e} | {f[i]: ^22.6e} |\n")

            file.write("-" * 61)

        # Отключаем интерактивный режим
        plt.ioff()

        fig, axs = plt.subplots(2, 3, figsize=(11, 7))

        # Первый график
        axs[0, 0].plot(z, f)
        axs[0, 0].set_title('F(z)')
        axs[0, 0].grid(True)

        # # Второй график
        axs[0, 1].plot(z, u)
        # axs[0, 1].plot(z, self.__system.u_p(z))
        axs[0, 1].set_title('u(z)')
        axs[0, 1].grid(True)

        # # Третий график
        axs[0, 2].plot(z, self.__system.u_p(z))
        axs[0, 2].set_title('u_p(z)')
        axs[0, 2].grid(True)

        # Сохраняем графики в файл
        fig.savefig(f"../data/{filename}.png")

        # Включаем интерактивный режим обратно
        plt.ion()
