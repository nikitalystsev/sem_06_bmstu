import math as m


def sample_mean(_x_n):
    return sum(_x_n) / len(_x_n)


def corrected_sample_variance(_x_n):
    _sum = 0
    _sample_mean = sample_mean(_x_n)

    for xi in _x_n:
        _sum += (xi - _sample_mean) ** 2

    return _sum / (len(_x_n) - 1)


def main():
    x_n = [5.4, -13.9, -11.0, 7.2, -15.6, 29.2, 1.4, -0.3, 6.6, -9.9]

    print(f"Выборочное среднее: {sample_mean(x_n)}")
    print(f"Исправленная выборочная дисперсия: {corrected_sample_variance(x_n)}")
    print(f"Корень из исправленной выборочной дисперсии: {m.sqrt(corrected_sample_variance(x_n))}")


if __name__ == '__main__':
    main()
