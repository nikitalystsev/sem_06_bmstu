import matplotlib.pyplot as plt
import numpy as np
from lsm_for_line import LeastSquaresMethodLine


class DataClass:
    """
    Класс данных и функций задачи второй лабораторной
    """

    def __init__(
            self,
            c: int = 3e10,  # отладочные значения
            r: int | float = 0.35,
            t_w: int = 2000,
            t_0: int = 1e4,
            p: int = 4
    ) -> None:
        """
        Инициализация атрибутов класса
        """
        self.__c = c
        self.__r = r
        self.__t_w = t_w
        self.__t_0 = t_0
        self.__p = p

        self.__orig_data_k1: dict = self.__read_k("../data/k1.txt")
        self.__orig_data_k2: dict = self.__read_k("../data/k2.txt")

        self.__log_data_k1, self.__a1, self.__b1 = self.__data_to_interp(self.__orig_data_k1)
        self.__log_data_k2, self.__a2, self.__b2 = self.__data_to_interp(self.__orig_data_k2)

        self.__plot_data()

    def t(self, z: int | float):
        """
        Функция нахождения температурного поля в цилиндре
        """
        t_z = (self.__t_w - self.__t_0) * z ** self.__p + self.__t_0

        return t_z

    def u_p(self, z: int | float):
        """
        Функция Планка
        """
        u_p_z = 3.084e-4 / (np.exp(4.799e4 / self.t(z)) - 1)

        return u_p_z

    def der_u(self, z, f):
        """
        Функция правой части первого уравнения
        f = f(z) - значение функции F в точке z
        """

        return - 3 * self.__r * self.k1(z) / self.__c * f

    def der_f(self, z, u, f):
        """
        Функция правой части первого уравнения
        f = f(z) - значение функции F в точке z
        u = u(z) - значение функции u в точке z
        """

        return -f / z + self.__r * self.__c * self.k1(z) * (self.u_p(z) - u)

    def k1(self, t: int | float | list | np.ndarray):
        """
        Функция для получения значения первого варианта коэффициента поглощения
        в точках между узлами
        """
        res = np.exp(self.__a1 * np.log(t) + self.__b1)

        return res

    def k2(self, t: int | float | list | np.ndarray):
        """
        Функция для получения значения первого варианта коэффициента поглощения
        в точках между узлами
        """

        res = np.exp(self.__a2 * np.log(t) + self.__b2)

        return res

    @property
    def c(self):
        return self.__c

    @staticmethod
    def __read_k(filename: str) -> dict:
        """
        Класс для считывания файла с данными коэффициента поглощения
        """
        data_k = dict()

        with open(filename) as file:
            for line in file:
                key, value = line.split()
                data_k[int(key)] = float(value)

        return data_k

    @staticmethod
    def __data_to_interp(orig_data_k: dict) -> tuple[dict, float, float]:
        """
        Метод интерполирует таблицу значений коэффициента поглощения прямой
        """
        log_data_k = dict()

        psi = np.log(list(orig_data_k.keys()))  # мб и не нужно
        teta = np.log(list(orig_data_k.values()))

        a, b = LeastSquaresMethodLine(x=psi, y=teta).get_solve()

        for i in range(len(orig_data_k)):
            log_data_k[psi[i]] = teta[i]

        return log_data_k, a, b

    def __plot_data(self):
        """
        Временный метод для построения графика
        """
        # fig1 = plt.figure(figsize=(10, 7))
        # plot = fig1.add_subplot()
        #
        # res = self.k1(list(self.__orig_data_k1.keys()))

        # print(res)
        # print(list(self.orig_data_k1.values()), res, sep='\n')

        # # plot.plot(self.data_k1.keys(), self.data_k1.values(), label="Первый вариант k")
        # plot.plot(self.orig_data_k1.keys(), self.orig_data_k1.values(), label="Первый вариант k (логарифм)")
        # plot.plot(self.__log_data_k1.keys(), res, label="Первый вариант k (логарифм) 2")
        # plot.plot(self.__log_data_k1.keys(), self.__log_data_k1.values(), label="первый вариант к (прямая)")

        # plt.legend()
        # plt.grid()
        #
        # plt.show()
