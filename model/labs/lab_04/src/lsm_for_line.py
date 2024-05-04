import numpy as np


class LeastSquaresMethodLine:
    """
    Класс для аппроксимации некоторой таблично заданной функции прямой
    """

    def __init__(self,
                 x: np.ndarray,
                 y: np.ndarray
                 ) -> None:
        """
        Инициализация атрибутов класса
        """
        self.__x = x
        self.__y = y
        self.__n = len(self.__x)

        self.__sum_x = sum(self.__x)
        self.__sum_y = sum(self.__y)
        self.__sum_x_squ = self.__get_sum_x_squ()
        self.__sum_xy = self.__get_sum_xy()

    def __get_sum_x_squ(self):
        """
        Метод для подсчета суммы квадратов значений аргумента
        """
        sum_x_squ = 0

        for x in self.__x:
            sum_x_squ += (x * x)

        return sum_x_squ

    def __get_sum_xy(self):
        """
        Метод для подсчета суммы произведений xy
        """
        sum_xy = 0

        for i in range(self.__n):
            sum_xy += (self.__x[i] * self.__y[i])

        return sum_xy

    def get_solve(self):
        """
        Метод для получения коэффициентов уравнения прямой
        уравнение прямой: y = a * x + b
        """
        b = (self.__sum_xy * self.__sum_x - self.__sum_y * self.__sum_x_squ) / (
                self.__sum_x ** 2 - self.__sum_x_squ * self.__n)

        a = (self.__sum_y - b * self.__n) / self.__sum_x

        return a, b
