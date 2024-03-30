from lsm_for_line import LeastSquaresMethodLine
import numpy as np


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

        # коэффициенты уравнения прямой
        self.__a1, self.__b1 = self.__data_to_interp(self.__orig_data_k1)
        self.__a2, self.__b2 = self.__data_to_interp(self.__orig_data_k2)

    def t(self, z: int | float):
        """
        Функция нахождения температурного поля в цилиндре
        """
        t_z = (self.__t_w - self.__t_0) * (z ** self.__p) + self.__t_0

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
        common_part = self.__r * self.__c * self.k1(z) * (self.u_p(z) - u)

        return -f / z + common_part if abs(z) > 1e-4 else common_part / 2

    def k1(self, t: int | float):
        """
        Функция для получения значения первого варианта коэффициента поглощения
        в точках между узлами
        """
        res = np.exp(self.__a1 * np.log(t) + self.__b1)

        return res

    def k2(self, t: int | float):
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
    def __data_to_interp(orig_data_k: dict) -> tuple[float, float]:
        """
        Метод интерполирует таблицу значений коэффициента поглощения прямой
        """
        psi = np.log(list(orig_data_k.keys()))
        teta = np.log(list(orig_data_k.values()))

        a, b = LeastSquaresMethodLine(x=psi, y=teta).get_solve()

        return a, b
