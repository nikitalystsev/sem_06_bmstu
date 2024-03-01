import matplotlib.pyplot as plt

BASE = "\x1B[0m"
GREEN = "\x1B[32m"
RED = "\x1B[31m"
YELLOW = "\x1B[33m"
BLUE = "\x1B[34m"
PURPLE = "\x1B[35m"

MAX_X = 2.003
STEP = 1e-4


def f(x, y):
    return pow(x, 2) + pow(y, 2)


def PicarApprox1(x):
    return pow(x, 3) / 3


def PicarApprox2(x):
    return PicarApprox1(x) + \
        pow(x, 7) / 63


def PicarApprox3(x):
    return PicarApprox2(x) + \
        2 * pow(x, 11) / 2079 + \
        pow(x, 15) / 59535


def PicarApprox4(x):
    return PicarApprox2(x) + \
        2 * pow(x, 11) / 2079 + \
        13 * pow(x, 15) / 218295 + \
        82 * pow(x, 19) / 37328445 + \
        662 * pow(x, 23) / 10438212015 + \
        4 * pow(x, 27) / 3341878155 + \
        pow(x, 31) / 109876903975


def Picar(x_max, h, PicarApprox):
    result = []
    x, y = 0, 0

    while abs(x) < abs(x_max):
        result.append(y)
        x += h
        y = PicarApprox(x)

    return result


def Euler(x_max, h):
    result = []
    x, y = 0, 0

    while abs(x) < abs(x_max):
        result.append(y)
        y = y + h * f(x, y)
        x += h

    return result


def RungeKutta(x_max, h):
    result = []
    coeff = h / 2
    x, y = 0, 0

    while abs(x) < abs(x_max):
        result.append(y)
        y = y + h * f(x + coeff, y + coeff * f(x, y))
        x += h

    return result


def generate_x(x_max, step):
    result = []
    x = 0

    while abs(x) < abs(x_max):
        result.append(round(x, 3))
        x += step

    return result


def print_res_table(x_arr, picar_approx1_arr, picar_approx2_arr,
                    picar_approx3_arr, picar_approx4_arr,
                    euler_arr, runge_kutta):
    print("\n%s  X   | PicarApprox1 | PicarApprox2 | PicarApprox3 | PicarApprox4 |     Euler    | RungeKutta \n"
          "-----------------------------------------------------------------------------------------------%s"
          % (PURPLE, BASE))

    for i in range(len(x_arr)):
        if i % 500 == 0:
            print("%5.2f %s|%s%12.5f  %s|%s%12.5f  %s|%s%12.5f  %s|%s%12.5f  %s|%s%12.5f  %s|%s%12.5f  " \
                  % (x_arr[i], PURPLE, BASE,
                     picar_approx1_arr[i], PURPLE, BASE,
                     picar_approx2_arr[i], PURPLE, BASE,
                     picar_approx3_arr[i], PURPLE, BASE,
                     picar_approx4_arr[i], PURPLE, BASE,
                     euler_arr[i], PURPLE, BASE,
                     runge_kutta[i]
                     ))

    print()


def build_graph(x_arr, picar_approx1_arr, picar_approx2_arr,
                picar_approx3_arr, picar_approx4_arr,
                euler_arr):
    fig1 = plt.figure(figsize=(10, 7))
    plot = fig1.add_subplot()
    plot.plot(x_arr, picar_approx1_arr, label="PicarApprox1")
    plot.plot(x_arr, picar_approx2_arr, label="PicarApprox2")
    plot.plot(x_arr, picar_approx3_arr, label="PicarApprox3")
    plot.plot(x_arr, picar_approx4_arr, label="PicarApprox4")
    plot.plot(x_arr, euler_arr, label="Euler")

    plt.legend()
    plt.grid()
    plt.title("Сравнение алгоритмом")

    plt.show()


def main():
    x_arr = generate_x(MAX_X, STEP)
    print(x_arr)
    picar_approx1_arr = Picar(MAX_X, STEP, PicarApprox1)
    picar_approx2_arr = Picar(MAX_X, STEP, PicarApprox2)
    picar_approx3_arr = Picar(MAX_X, STEP, PicarApprox3)
    picar_approx4_arr = Picar(MAX_X, STEP, PicarApprox4)
    euler_arr = Euler(MAX_X, STEP)
    runge_kutta = RungeKutta(MAX_X, STEP)

    print_res_table(x_arr, picar_approx1_arr, picar_approx2_arr,
                    picar_approx3_arr, picar_approx4_arr,
                    euler_arr, runge_kutta)

    x_arr = generate_x(-MAX_X, -STEP)
    x_arr.reverse()
    x_arr.extend(generate_x(MAX_X, STEP))

    picar_approx1_arr = Picar(-MAX_X, -STEP, PicarApprox1)
    picar_approx1_arr.reverse()
    picar_approx1_arr.extend(Picar(MAX_X, STEP, PicarApprox1))

    picar_approx2_arr = Picar(-MAX_X, -STEP, PicarApprox2)
    picar_approx2_arr.reverse()
    picar_approx2_arr.extend(Picar(MAX_X, STEP, PicarApprox2))

    picar_approx3_arr = Picar(-MAX_X, -STEP, PicarApprox3)
    picar_approx3_arr.reverse()
    picar_approx3_arr.extend(Picar(MAX_X, STEP, PicarApprox3))

    picar_approx4_arr = Picar(-MAX_X, -STEP, PicarApprox4)
    picar_approx4_arr.reverse()
    picar_approx4_arr.extend(Picar(MAX_X, STEP, PicarApprox4))

    euler_arr = Euler(-MAX_X, -STEP)
    euler_arr.reverse()
    euler_arr.extend(Euler(MAX_X, STEP))

    runge_kutta = RungeKutta(-MAX_X, -STEP)
    runge_kutta.reverse()
    runge_kutta.extend(RungeKutta(MAX_X, STEP))

    build_graph(x_arr, picar_approx1_arr, picar_approx2_arr,
                picar_approx3_arr, picar_approx4_arr,
                euler_arr)


if __name__ == "__main__":
    main()
