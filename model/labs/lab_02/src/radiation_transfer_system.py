from lsm_for_line import LeastSquaresMethodLine
import numpy as np
from dataclasses import dataclass

EPS = 1e-4


@dataclass
class RadiationTransferSystem:
    """
    Класс данных и функций задачи второй лабораторной
    """
    __orig_data_k1: dict = None
    __orig_data_k2: dict = None
    __a1: int | float = None
    __b1: int | float = None
    __a2: int | float = None
    __b2: int | float = None
    # параметры для отладки (переписал правильно)
    __c: int = 3e10
    __r: int | float = 0.35
    __t_w: int = 2000
    __t_0: int = 1e4
    __p: int = 4

    def __post_init__(self):
        """
        Пост-инициализация атрибутов класса
        """
        self.__orig_data_k1 = self.__read_k("../data/k1.txt")
        self.__orig_data_k2 = self.__read_k("../data/k2.txt")
        self.__a1, self.__b1 = self.__data_to_interp(self.__orig_data_k1)
        self.__a2, self.__b2 = self.__data_to_interp(self.__orig_data_k1)

    def t(self, z: int | float):
        """
        Функция нахождения значения температурного поля в цилиндре
        """
        t_z = (self.__t_w - self.__t_0) * (z ** self.__p) + self.__t_0

        return t_z

    def u_p(self, z: int | float):
        """
        Функция Планка
        """
        u_p_z = 3.084e-4 / (np.exp(4.799e4 / self.t(z)) - 1)

        return u_p_z

    def der_u(self, z, f, is_k1=True):
        """
        Функция правой части первого уравнения
        f = f(z) - значение функции F в точке z
        """
        # мда, треш, долго доходило, что не k(z), а k(t(z))
        if is_k1:
            res = -3 * self.__r * self.k1(self.t(z)) / self.__c * f
        else:
            res = -3 * self.__r * self.k2(self.t(z)) / self.__c * f

        return res

    def der_f(self, z, u, f, is_k1=True):
        """
        Функция правой части первого уравнения
        f = f(z) - значение функции F в точке z
        u = u(z) - значение функции u в точке z
        """

        if is_k1:
            common_part = self.__r * self.__c * self.k1(self.t(z)) * (self.u_p(z) - u)
        else:
            common_part = self.__r * self.__c * self.k2(self.t(z)) * (self.u_p(z) - u)

        return -f / z + common_part if abs(z) > EPS else common_part / 2

    def k1(self, t: int | float):
        """
        Функция для получения значения первого варианта коэффициента поглощения
        в точках между узлами
        """
        res = np.exp(self.__a1 * np.log(t) + self.__b1)

        return res

    def k2(self, t: int | float):
        """
        Функция для получения значения второго варианта коэффициента поглощения
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

    @staticmethod
    def __print_dict(_dict: dict) -> None:
        """
        Вывод словаря
        """
        for key, value in _dict.items():
            print(f"{key}: {value}")
