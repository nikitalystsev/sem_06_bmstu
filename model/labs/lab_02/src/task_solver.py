from data_class import DataClass
import numpy as np

EPS = 1e-4


class TaskSolver:
    """
    Класс для решения задачи второй лабораторной
    """

    def __init__(
            self
    ) -> None:
        # 0 <= z <= 1
        self.__a = 0
        self.__b = 1

        self.__n = 100  # число узлов
        self.__h = (self.__b - self.__a) / self.__n  # шаг

        self.__f_0 = 0
        self.__u_0 = self.__get_u_0()

        self.__data_class = DataClass()  # c отладочными параметрами

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

        z_res = np.arange(self.__a, self.__b + half_h, self.__h)
        u_res = np.zeros(len(z_res))
        f_res = np.zeros(len(z_res))

        u_n = u_0
        f_n = f_0

        for i, z in enumerate(z_res):
            u_res[i] = u_n
            f_res[i] = f_n

            k1 = self.__data_class.der_u(z, f_n)
            q1 = self.__data_class.der_f(z, u_n, f_n)

            k2 = self.__data_class.der_u(z + half_h, f_n + half_h * q1)
            q2 = self.__data_class.der_f(z + half_h, u_n + half_h * k1, f_n + half_h * q1)

            u_n += self.__h * ((alpha - 1) * k1 + alpha * k2)
            f_n += self.__h * ((alpha - 1) * q1 + alpha * q2)

        return z_res, u_res, f_res

    def __get_psi(self, u, f):
        """
        Функция правого краевого условия
        """

        return f - 0.393 * self.__data_class.c * u

    def __get_step_solve(self, psi):
        """
        Функция для определения решений задачи Коши методом Рунге Кутта 2 порядка точности
        для текущего параметра psi
        """
        _, u, f = self.runge_kutta2(
            psi * self.__data_class.u_p(0),
            self.__f_0
        )

        # нужно смотреть удовлетворение правому краевому условию
        res = self.__get_psi(u[-1], f[-1])

        return res

    def __get_ksi_interval(self, a, b, h: int | float):
        """
        Функция что то делает
        """
        psi_from, psi_to = self.__get_step_solve(a), self.__get_step_solve(a + h)
        ksi_from, ksi_to = a, a + h

        while ksi_to < b - h / 2 and psi_from * psi_to > 0:
            ksi_from = ksi_to
            ksi_to += h

            psi_from = psi_to
            psi_to = self.__get_step_solve(ksi_to)

        return ksi_from, ksi_to

    def __get_ksi(self, a, b, h: int | float):
        """
        Что-то делает
        """
        ksi_from, ksi_to = self.__get_ksi_interval(a, b, h)

        print(f"ksi interval ({ksi_from}, {ksi_to})")

        ksi_curr = ksi_from - ksi_to

        iter_num = 0

        while abs((ksi_from - ksi_to) / ksi_curr) > EPS and iter_num < 100:
            ksi_curr = (ksi_from + ksi_to) / 2

            if self.__get_step_solve(ksi_from) * self.__get_step_solve(ksi_curr) < 0:
                ksi_to = ksi_curr
            else:
                ksi_from = ksi_curr

            iter_num += 1

        return ksi_curr

    def __get_u_0(self):
        """
        Метод для подбора начального условия, чтобы
        удовлетворяло правому краевому условию
        """
        # диапазоны значений для psi
        ksi_a = 0
        ksi_b = 1

        n = 100  # число узлов
        h = (ksi_b - ksi_a) / n  # шаг

        return self.__get_ksi(ksi_a, ksi_b, h) * self.__data_class.u_p(0)

    def get_solve(self):
        """
        Метод получает решение методом Рунге-Кутта 2-го порядка точности
        """
        return self.runge_kutta2(self.__u_0, self.__f_0)
