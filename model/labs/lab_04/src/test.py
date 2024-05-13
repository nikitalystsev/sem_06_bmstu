from numpy import e
import matplotlib.pyplot as plt
import numpy as np
from math import fabs, sin, pi
from mpl_toolkits.mplot3d import Axes3D
from prettytable import PrettyTable

ti_max = 500
data = {
    "k0": 1,
    'a1': 0.0134,
    'b1': 1,
    'c1': 4.35e-4,
    'm1': 1,
    'a2': 2.049,
    'b2': 0.563e-3,
    'c2': 0.528e5,
    'm2': 1,
    "alpha0": 0.05,
    "alphaN": 0.01,
    "l": 10,
    "T0": 300,
    "R": 0.5,
    "Fmax": 200,
    "tmax": 60,
    'tau': 1,
    'h': 1e-2,
    'x0': 0,
    'period': 1,
    'tu': 0.9
}


class Function:
    def __init__(self):
        self.k0 = data['k0']
        self.a1 = data['a1']
        self.b1 = data['b1']
        self.c1 = data['c1']
        self.m1 = data['m1']
        self.a2 = data['a2']
        self.b2 = data['b2']
        self.c2 = data['c2']
        self.m2 = data['m2']
        self.l = data['l']
        self.T0 = data['T0']
        self.R = data['R']
        self.tau = data['tau']

        self.x0 = data['x0']

        self.alpha0 = data['alpha0']
        self.alphaN = data['alphaN']

        self.Fmax = data['Fmax']
        self.tmax = data['tmax']

        self.h = data['h']
        self.XEPS = 1
        self.TEPS = 1e-4

    def alpha(self, x):
        d = (self.alphaN * self.l) / (self.alphaN - self.alpha0)
        c = -self.alpha0 * d
        return c / (x - d)

    def p(self, x):
        return 2 * self.alpha(x) / self.R

    def k(self, T):
        return self.k0 * ((T / 300) ** 2)

    def Lambda(self, T):
        return self.a1 * (self.b1 + self.c1 * T ** self.m1)

    def C(self, T):
        return self.a2 + self.b2 * T ** self.m2 - (self.c2 / T ** 2)

    def f2(self, x):
        return 2 * self.T0 * self.alpha(x) / self.R

    def F0(self, t):
        period = data['period']
        tu = data['tu']
        # if (t % period <= tu):
        # return self.Fmax / self.tmax * t * e**(-(t / self.tmax - 1))
        # return self.Fmax / self.tmax * t * e**(-(t / self.tmax - 1))
        return 10


class Lab4(Function):
    def A(self, T, n):
        return (self.tau * (self.Lambda(T[n]) + self.Lambda(T[n - 1]))
                / self.h / 2)

    def D(self, T, n):
        return (self.tau * (self.Lambda(T[n]) + self.Lambda(T[n + 1]))
                / self.h / 2)

    def B(self, x, T, n):
        return (self.A(T, n) + self.D(T, n) + self.C(T[n]) * self.h +
                self.p(x) * self.tau * self.h)

    def G(self, x, T, n, ti):
        g1 = self.C(T[n]) * self.h * T[n]
        g2 = (self.h * self.tau * self.k(T[n])
              * self.F0(ti) * e ** (-self.k(T[n]) * x))
        g3 = self.f2(x) * self.h * self.tau

        return g1 + g2 + g3

    def leftBC(self, Tprev, time):
        h = self.h
        k1 = h * (self.C(Tprev[0]) + self.C(Tprev[1])) / 16
        k2 = h * self.C(Tprev[0]) / 4
        k3 = self.tau * (self.Lambda(Tprev[0]) + self.Lambda(Tprev[1])) / h / 2
        k4 = self.tau * h * (self.p(0) + self.p(h)) / 16
        k5 = self.tau * h * self.p(0) / 4
        k6 = self.alpha0 * self.tau
        K0 = k1 + k2 + k3 + k4 + k5 + k6

        m1 = h * (self.C(Tprev[0]) + self.C(Tprev[1])) / 16
        m2 = self.tau * (self.Lambda(Tprev[0]) + self.Lambda(Tprev[1])) / h / 2
        m3 = self.tau * h * (self.p(0) + self.p(h)) / 16
        M0 = m1 - m2 + m3

        p1 = (h * (self.C(Tprev[0]) + self.C(Tprev[1]))
              * (Tprev[0] + Tprev[1]) / 16)
        p2 = h * self.C(Tprev[0]) * Tprev[0] / 4
        p3 = self.alpha0 * self.T0 * self.tau
        p4 = (self.T0 / self.R
              * (3 * self.alpha0 + self.alpha(h)) * h * self.tau / 4)
        p5 = (h * self.tau * self.F0(time) * self.k(Tprev[0]) / 4)
        p6 = (h * self.tau * self.F0(time) * (self.k(Tprev[0]) +
                                              self.k(Tprev[1])) * e ** (-(self.k(Tprev[0]) +
                                                                          self.k(Tprev[1])) * (h / 2)) / 16)

        P0 = p1 + p2 + p3 + p4 + p5 + p6

        return K0, M0, P0

    def rightBC(self, Tprev, time):
        h = self.h
        k1 = h * self.C(Tprev[-1]) / 4
        k2 = h * (self.C(Tprev[-1]) + self.C(Tprev[-2])) / 16
        k3 = (self.tau * (self.Lambda(Tprev[-1]) + self.Lambda(Tprev[-2]))
              / h / 2)
        k4 = self.tau * h * self.p(self.l) / 4
        k5 = self.tau * h * (self.p(self.l) + self.p(self.l - h)) / 16
        k6 = - self.alphaN * self.tau
        KN = k1 + k2 + k3 + k4 + k5 + k6

        m1 = h * (self.C(Tprev[-1]) + self.C(Tprev[-2])) / 16
        m2 = (self.tau * (self.Lambda(Tprev[-1]) + self.Lambda(Tprev[-2]))
              / h / 2)
        m3 = self.tau * h * (self.p(self.l) + self.p(self.l - h)) / 16
        MN = m1 - m2 + m3

        p1 = (h * (self.C(Tprev[-1]) + self.C(Tprev[-2]))
              * (Tprev[-1] + Tprev[-2]) / 16)
        p2 = - self.tau * self.alphaN * self.T0
        p3 = self.tau * h * (3 * self.f2(self.l) + self.f2(self.l - h)) / 8
        p4 = h * self.C(Tprev[-1]) * Tprev[-1] / 4
        p5 = (h * self.tau * self.F0(time) * self.k(Tprev[-1])
              * e ** (-self.k(Tprev[-1]) * self.l) / 4)
        p6 = (h * self.tau * self.F0(time) * (self.k(Tprev[-1]) +
                                              self.k(Tprev[-2])) * e ** (-(self.k(Tprev[-1]) +
                                                                           self.k(Tprev[-2])) * (self.l - h / 2)) / 16)
        PN = p1 + p2 + p3 + p4 + p5 + p6

        return KN, MN, PN

    def run(self, Tprev, ti):
        h = self.h
        K0, M0, P0 = self.leftBC(Tprev, ti)
        KN, MN, PN = self.rightBC(Tprev, ti)

        eps = [0, -M0 / K0]
        eta = [0, P0 / K0]
        x = h
        n = 1

        while (x < self.l - h / 2):
            eps.append(self.D(Tprev, n) / (self.B(x, Tprev, n)
                                           - self.A(Tprev, n) * eps[n]))
            eta.append((self.G(x, Tprev, n, ti) + self.A(Tprev, n) * eta[n])
                       / (self.B(x, Tprev, n) - self.A(Tprev, n) * eps[n]))
            n += 1
            x += h

        y = [0] * (n + 1)
        y[n] = (PN - MN * eta[n]) / (KN + MN * eps[n])

        for i in range(n - 1, -1, -1):
            y[i] = eps[i + 1] * y[i + 1] + eta[i + 1]

        return y


class Table(PrettyTable):
    def add_columns(self, colDict: dict):
        for key, value in colDict.items():
            self.add_column(key, value[0], align="r")
            self.custom_format[key] = value[1]


class Graphics:
    def __init__(self, graphics=[]):
        self.graphics = graphics
        self.num = len(graphics)

    def addGraphiC(self, xVals, yVals, labels, title):
        self.graphics.append({
            "x": xVals,
            "y": yVals,
            "labels": labels,
            "title": title
        })
        self.num += 1

    def show(self):
        for i, graph in enumerate(self.graphics):
            plt.subplot(2, self.num // 2 + self.num % 2, i + 1)

            for j, y in enumerate(graph["y"]):
                plt.plot(graph["x"], y, label=graph["labels"][j])

            plt.legend()
            plt.title(graph["title"])
            plt.grid()

        plt.subplots_adjust(wspace=0.3, hspace=0.3)
        plt.show()


class Res(Lab4):
    def res(self):
        h = self.h
        lenTx = int(self.l / h)
        T = [self.T0] * (lenTx + 1)

        ti = 0
        res = []
        res.append(T)

        while True:
            prev = T
            ti += self.tau

            diffByTMax = self.XEPS + h
            while diffByTMax > self.XEPS:
                Tnew = self.run(prev, ti)
                diffByTMax = abs((T[0] - Tnew[0]) / Tnew[0])

                for curTPrev, curTNew in zip(T, Tnew):
                    curDiff = abs((curTPrev - curTNew) / curTNew)

                    if curDiff > diffByTMax:
                        diffByTMax = curDiff

                prev = Tnew

            res.append(Tnew)

            check_eps = 0
            for i, j in zip(T, Tnew):

                if fabs((i - j) / j) > self.TEPS:
                    check_eps = 1

            if check_eps == 0:
                break

            T = Tnew

        return res, ti

    def draw(self):
        h = self.h
        res, ti = self.res()
        x = [i for i in np.arange(0, self.l, h)]
        te = [i for i in np.arange(0, ti, self.tau)]

        # 3д график
        xgrid, ygrid = np.meshgrid(x, te)
        zgrid = [i[:-1] for i in res]
        zgrid.pop()
        xgrid = np.array(xgrid)
        ygrid = np.array(ygrid)
        zgrid = np.array(zgrid)

        # fig = plt.figure(figsize=(7, 4))
        # ax_3d = Axes3D(fig)
        # ax_3d.plot_surface(ygrid, xgrid, zgrid, cmap='GnBu')
        # ax_3d.set_ylabel("x, cm")
        # ax_3d.set_xlabel("t, c")
        # ax_3d.set_zlabel("T, K")
        # plt.show()

        # Построение графика
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(ygrid, xgrid, zgrid, cmap='viridis')

        # Настройка подписей осей
        ax.set_xlabel('x')
        ax.set_ylabel('t')
        ax.set_zlabel('T(x, t)')
        ax.set_title('Температурное поле')
        plt.show()

    #     # группа 2д графиков
    #     plt.subplot(2, 1, 1)
    #     step1 = 0
    #     for_graph = ti_max / 10
    #     for i in res:
    #         if (step1 % for_graph == 0):
    #             namestr = "t = " + str(step1)
    #             plt.plot(x, i[:-1], label=namestr)
    #         step1 += 1
    #
    #     plt.plot(x, res[-1][:-1])
    #     plt.xlabel("x, cm")
    #     plt.ylabel("T, K")
    #     plt.legend()
    #     plt.grid()
    #
    #     plt.subplot(2, 1, 2)
    #     step2 = 0
    #     iter = 0
    #     l = int(self.l / self.h)
    #     while iter < 10:
    #         point = [j[int(step2 / h)] for j in res]
    #         namestr = "x = " + str(round(step2, 1))
    #         plt.plot(te, point[:-1], label=namestr)
    #         step2 += 0.1 * 10
    #         iter += 1
    #
    #     plt.xlabel("t, sec")
    #     plt.ylabel("T, K")
    #     plt.grid()
    #
    #     plt.show()
    #
    # def step_t(self):
    #     h = self.h
    #     deltah = [1, 0.1, 0.01, 0.001]
    #     result = []
    #     for hi in deltah:
    #         self.tau = hi
    #         res, ti = self.res()
    #
    #         n = 0
    #         for temp in res:
    #             if (fabs(n - 1) < self.TEPS):
    #                 print()
    #                 print(self.tau)
    #                 print()
    #                 result.append(temp[:-1])
    #             n += self.tau
    #     print('    1    |   0.1   |   0.01  |  0.001  |')
    #     for i in range(len(result[0])):
    #         for j in range(len(result)):
    #             print(' %3.3f |' % result[j][i], end='')
    #         print()
    #
    # def step_t2(self):
    #     deltah = [1, 0.1, 0.01, 0.001]
    #     result = []
    #     for hi in deltah:
    #         self.h = hi
    #         h = self.h
    #         res, ti = self.res()
    #         print(h)
    #         i = 0
    #         xfix = [temp[int(i / h)] for temp in res]
    #         result.append(xfix)
    #
    #     print('    1    |   0.1   |   0.01  |  0.001  |')
    #     for i in range(len(result[0])):
    #         for j in range(len(result)):
    #             print(' %3.3f |' % result[j][i], end='')
    #         print()
    #
    # def a_b(self):
    #     h = self.h
    #     t = self.tau
    #     arraya2 = [2.049, 5, 10, 15, 50]
    #     arrayb2 = [0.000564, 0.001, 0.01, 0.1, 5]
    #     result = []
    #     resulti = []
    #     for ai, bi in zip(arraya2, arrayb2):
    #         self.a2 = ai
    #         self.b2 = bi
    #         res, ti = self.res()
    #
    #         te = []
    #         i = 0
    #         while (i < ti):
    #             te.append(i)
    #             i += t
    #
    #         i = 0
    #         xfix = [temp[int(i / h)] for temp in res]
    #         print(xfix[:-1])
    #         result.append(xfix[:-1])
    #         resulti.append(te)
    #
    #     for res, teres in zip(result, resulti):
    #         plt.plot(teres, res)
    #
    #     plt.xlabel("Время, c")
    #     plt.ylabel("Температура, K")
    #     plt.show()
    #
    # def chast(self):  # надо поменять в F0: return 0 поставить
    #     res, ti = self.res()
    #
    #     te = []
    #     i = 0
    #     while (i < ti):
    #         te.append(i)
    #         i += self.tau
    #     i = 0
    #     xfix = [temp[int(i / self.h)] for temp in res]
    #     plt.plot(te, xfix[1:])
    #     plt.xlabel("Время, c")
    #     plt.ylabel("Температура, K")
    #     plt.show()


def main():
    resh = Res()
    print(resh.draw())
    # resh.chast()


if __name__ == "__main__":
    main()
