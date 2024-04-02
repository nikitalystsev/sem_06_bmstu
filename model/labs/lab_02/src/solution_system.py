from radiation_transfer_system import RadiationTransferSystem
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

EPS = 1e-4


class SolutionSystem:
    """
    Класс для решения задачи второй лабораторной
    """

    def __init__(
            self
    ) -> None:
        # класс системы уравнений
        self.__system = RadiationTransferSystem()

        # 0 <= z <= 1
        self.__a = 0
        self.__b = 1

        self.__n = 1e5  # число узлов
        self.__h = (self.__b - self.__a) / self.__n  # шаг

        print(f"h = {self.__h}")

        self.__f_0 = 0
        self.__u_0 = self.__get_u_0()

    def runge_kutta2(
            self,
            u_0: int | float,  # параметры - начальные условия задачи Коши
            f_0: int | float
    ):
        """
        Реализация метода Рунге Кутта 2-го порядка
        """
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

            k1 = self.__system.der_u(z, f_n)
            q1 = self.__system.der_f(z, u_n, f_n)

            k2 = self.__system.der_u(z + half_h, f_n + half_h * q1)
            q2 = self.__system.der_f(z + half_h, u_n + half_h * k1, f_n + half_h * q1)

            u_n += self.__h * ((alpha - 1) * k1 + alpha * k2)
            f_n += self.__h * ((alpha - 1) * q1 + alpha * q2)

        return z_res, u_res, f_res

    def runge_kutta4(
            self,
            u_0: int | float,  # параметры - начальные условия задачи Коши
            f_0: int | float
    ):
        """
        Реализация метода Рунге Кутта 4-го порядка
        """
        is_k1 = True
        # is_k1 = True

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

            # print(f"k1 = {k1}")
            k2 = self.__system.der_u(z + half_h, f_n + half_h * q1, is_k1=is_k1)
            q2 = self.__system.der_f(z + half_h, u_n + half_h * k1, f_n + half_h * q1, is_k1=is_k1)

            k3 = self.__system.der_u(z + half_h, f_n + half_h * q2, is_k1=is_k1)
            q3 = self.__system.der_f(z + half_h, u_n + half_h * k2, f_n + half_h * q2, is_k1=is_k1)

            k4 = self.__system.der_u(z + self.__h, f_n + self.__h * q3, is_k1=is_k1)
            q4 = self.__system.der_f(z + self.__h, u_n + self.__h * k3, f_n + self.__h * q3, is_k1=is_k1)

            u_n += (self.__h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
            f_n += (self.__h / 6) * (q1 + 2 * q2 + 2 * q3 + q4)

        return z_res, u_res, f_res

    def __get_psi(self, u, f):
        """
        Функция правого краевого условия
        """

        return f - 0.393 * self.__system.c * u

    def __get_step_solve(self, psi):
        """
        Функция для определения решений задачи Коши методом Рунге Кутта 2 порядка точности
        для текущего параметра psi
        """
        _, u, f = self.runge_kutta4(psi * self.__system.u_p(0), self.__f_0)

        # нужно смотреть удовлетворение правому краевому условию
        res = self.__get_psi(u[-1], f[-1])

        return res

    def __get_scipy_step_solve(self, psi):
        """
        Функция для определения решений задачи Коши c пом. мат. пакета
        """
        _, u, f = self.__scipy_solution(psi * self.__system.u_p(0), self.__f_0)

        # нужно смотреть удовлетворение правому краевому условию
        res = self.__get_psi(u[-1], f[-1])

        return res

    @staticmethod
    def __get_ksi(a, b, func_step_solve):
        """
        Методом дихотомии (половинного деления) ищется корень уравнения
        psi(u(b, s), F(b, s)) = 0, где s - начальное значение в методе стрельбы
        """
        ksi_from, ksi_to = a, b  # начальный интервал неопределенности

        ksi_curr = 0

        condition = True

        count_iter = 0

        while condition:
            ksi_curr = (ksi_from + ksi_to) / 2  # находим середину текущего интервала неопределенности

            if func_step_solve(ksi_from) * func_step_solve(ksi_curr) < 0:
                ksi_to = ksi_curr
            if func_step_solve(ksi_curr) * func_step_solve(ksi_to) < 0:
                ksi_from = ksi_curr

            count_iter += 1

            if abs((ksi_to - ksi_from) / ksi_curr) <= EPS:
                condition = False

        print(f"ksi принадлежит интервалу ({ksi_from: <10.7f}, {ksi_to: 10.7f})")
        print(f"ksi_curr = {ksi_curr}")

        return ksi_curr

    def __get_u_0(self):
        """
        Метод для подбора начального условия, чтобы
        удовлетворяло правому краевому условию
        """
        # диапазоны значений для psi
        ksi_a = 1e-2
        ksi_b = 1

        res = self.__get_ksi(ksi_a, ksi_b, self.__get_scipy_step_solve) * self.__system.u_p(0)

        return res

    def __scipy_solution(
            self,
            u_0: int | float,  # параметры - начальные условия задачи Коши
            f_0: int | float
    ):
        """
        Метод для решения поставленной задачи с помощью мат. пакета
        """
        # is_k1 = True
        is_k1 = False

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

    def solve(self):
        """
        Метод для получения решения
        """

        # z, u, f = self.runge_kutta4(self.__u_0, self.__f_0)
        z, u, f = self.__scipy_solution(self.__u_0, self.__f_0)
        # self.__scipy_solution(self.__u_0, self.__f_0)
        # print(f"u = {u}")
        # Создание графиков
        fig, axs = plt.subplots(2, 3, figsize=(11, 7))

        # Первый график
        axs[0, 0].plot(z, f)
        axs[0, 0].set_title('F(z)')
        axs[0, 0].grid(True)

        # # Второй график
        axs[0, 1].plot(z, u)
        axs[0, 1].set_title('u(z)')
        axs[0, 1].grid(True)

        # # Третий график
        axs[0, 2].plot(z, self.__system.u_p(z))
        axs[0, 2].set_title('u_p(z)')
        axs[0, 2].grid(True)

        # # Четвертый график
        # axs[1, 0].plot(x4, y4)
        # axs[1, 0].set_title('График 4')
        #
        # # Пятый график
        # axs[1, 1].plot(x5, y5)
        # axs[1, 1].set_title('График 5')
        #
        # # Шестой график
        # axs[1, 2].plot(x6, y6)
        # axs[1, 2].set_title('График 6')

        plt.tight_layout()
        plt.show()
