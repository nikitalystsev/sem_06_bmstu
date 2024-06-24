import numpy as np
import matplotlib.pyplot as plt
from prettytable import PrettyTable

color = '#BA55D3'
color2 = '#FF69B4'
color3 = '#C71585'

EPS = 1e-1

x_min = 0
x_max = 10

z_min = 0
z_max = 10

Hx_COUNT = 101
Hx = (x_max - x_min) / (Hx_COUNT - 1)

Hz_COUNT = 101
Hz = (z_max - z_min) / (Hz_COUNT - 1)

TAU = 5

a1 = 0.0134
b1 = 1
c1 = 4.35e-4
m1 = 1

U0 = 300

alpha_1 = 1
alpha_2 = 1
alpha_3 = 1
alpha_4 = 1

f0 = 30
beta = 1
x0 = 1
z0 = 9.1


# ===========================================================================================================================

def lambda_n(u):
    return a1 * (b1 + c1 * np.power(u, m1))


def kappa(u1, u2):
    return (lambda_n(u1) + lambda_n(u2)) / 2


def f_n(x, z):
    return f0 * np.exp(-beta * (np.power(x - x0, 2) + np.power(z - z0, 2)))


# ===========================================================================================================================

def Ax(u1, u2):
    # kappa_minus(x)
    return kappa(u1, u2) * Hz * TAU / Hx


def Cx(u1, u2):
    # kappa_plus(x)
    return kappa(u1, u2) * Hz * TAU / Hx


def Bx(u1, u2, u3):
    return Ax(u1, u2) + Cx(u2, u3) + Hz * Hx


def Dx(x, z, prev_u):
    return prev_u * Hx * Hz + f_n(x, z) * Hx * Hz * TAU / 2


# ===========================================================================================================================

def Az(u1, u2):
    # kappa_minus(x)
    return kappa(u1, u2) * Hx * TAU / Hz


def Cz(u1, u2):
    # kappa_plus(x)
    return kappa(u1, u2) * Hx * TAU / Hz


def Bz(u1, u2, u3):
    return Az(u1, u2) + Cz(u2, u3) + Hz * Hx


def Dz(x, z, prev_u):
    return prev_u * Hx * Hz + f_n(x, z) * Hx * Hz * TAU / 2


# ===========================================================================================================================

def left_boundary_condition_x(x, z, u0, u1, prev_y0, prev_y1):
    f_n_half = (f_n(x, z) + f_n(x + Hx, z)) / 2

    K0 = Hx * Hz / 8 + Hx * Hz / 4 + kappa(u0, u1) * Hz * TAU / Hx + alpha_1 * TAU * Hz
    M0 = Hx * Hz / 8 - kappa(u0, u1) * Hz * TAU / Hx
    P0 = Hx * Hz / 8 * (prev_y0 + prev_y1) + Hx * Hz / 4 * prev_y0 + TAU * Hx * Hz / 8 * (
                f_n(x, z) + f_n_half) + alpha_1 * TAU * Hz * U0

    return K0, M0, P0


def right_boundary_condition_x(x, z, uN, u1, prev_yN, prev_y1):
    f_n_half = (f_n(x, z) + f_n(x - Hx, z)) / 2

    KN = Hx * Hz / 8 - kappa(uN, u1) * Hz * TAU / Hx
    MN = Hx * Hz / 8 + Hx * Hz / 4 + kappa(uN, u1) * Hz * TAU / Hx + alpha_2 * TAU * Hz
    PN = Hx * Hz / 8 * (prev_yN + prev_y1) + Hx * Hz / 4 * prev_yN + TAU * Hx * Hz / 8 * (
                f_n(x, z) + f_n_half) + alpha_2 * TAU * Hz * U0

    return KN, MN, PN


# ===========================================================================================================================

def left_boundary_condition_z(x, z, u0, u1, prev_y0, prev_y1):
    f_n_half = (f_n(x, z) + f_n(x, z + Hz)) / 2

    K0 = Hx * Hz / 8 + Hx * Hz / 4 + kappa(u0, u1) * Hx * TAU / Hz + alpha_3 * TAU * Hx
    M0 = Hx * Hz / 8 - kappa(u0, u1) * Hx * TAU / Hz
    P0 = Hx * Hz / 8 * (prev_y0 + prev_y1) + Hx * Hz / 4 * prev_y0 + TAU * Hx * Hz / 8 * (
                f_n(x, z) + f_n_half) + alpha_3 * TAU * Hx * U0

    return K0, M0, P0


def right_boundary_condition_z(x, z, uN, u1, prev_yN, prev_y1):
    f_n_half = (f_n(x, z) + f_n(x, z - Hz)) / 2

    KN = Hx * Hz / 8 - kappa(uN, u1) * Hx * TAU / Hz
    MN = Hx * Hz / 8 + Hx * Hz / 4 + kappa(uN, u1) * Hx * TAU / Hz + alpha_4 * TAU * Hx
    PN = Hx * Hz / 8 * (prev_yN + prev_y1) + Hx * Hz / 4 * prev_yN + TAU * Hx * Hz / 8 * (
                f_n(x, z) + f_n_half) + alpha_4 * TAU * Hx * U0

    return KN, MN, PN


# ===========================================================================================================================

def right_hand_run_method_x(z, u, prev_u):
    K0, M0, P0 = left_boundary_condition_x(x_min, z, u[0], u[1], prev_u[0], prev_u[1])
    KN, MN, PN = right_boundary_condition_x(x_max, z, u[-1], u[-2], prev_u[-1], prev_u[-2])

    xi = [0, -M0 / K0]
    eta = [0, P0 / K0]

    x = x_min + Hx

    n = 1

    # Прямой ход
    while x < x_max - Hx / 2:
        xi.append(Cx(u[n + 1], u[n]) / (Bx(u[n - 1], u[n], u[n + 1]) - Ax(u[n - 1], u[n]) * xi[n]))
        eta.append((Ax(u[n - 1], u[n]) * eta[n] + Dx(x, z, prev_u[n])) / (
                    Bx(u[n - 1], u[n], u[n + 1]) - Ax(u[n - 1], u[n]) * xi[n]))
        n += 1
        x += Hx

    n += 1

    # Обратный ход
    new_u = [0] * (n)
    new_u[n - 1] = (PN - KN * eta[n - 1]) / (MN + KN * xi[n - 1])

    for i in range(n - 2, -1, -1):
        new_u[i] = xi[i + 1] * new_u[i + 1] + eta[i + 1]

    return new_u


# ===========================================================================================================================

def right_hand_run_method_z(x, u, prev_u):
    K0, M0, P0 = left_boundary_condition_z(x, z_min, u[0], u[1], prev_u[0], prev_u[1])
    KN, MN, PN = right_boundary_condition_z(x, z_max, u[-1], u[-2], prev_u[-1], prev_u[-2])

    xi = [0, -M0 / K0]
    eta = [0, P0 / K0]

    z = z_min + Hz

    n = 1

    # Прямой ход
    while z < z_max - Hz / 2:
        xi.append(Cz(u[n + 1], u[n]) / (Bz(u[n - 1], u[n], u[n + 1]) - Az(u[n - 1], u[n]) * xi[n]))
        eta.append((Az(u[n - 1], u[n]) * eta[n] + Dz(x, z, prev_u[n])) / (
                    Bz(u[n - 1], u[n], u[n + 1]) - Az(u[n - 1], u[n]) * xi[n]))
        n += 1
        z += Hz

    n += 1

    # Обратный ход
    new_u = [0] * (n)
    new_u[n - 1] = (PN - KN * eta[n - 1]) / (MN + KN * xi[n - 1])

    for i in range(n - 2, -1, -1):
        new_u[i] = xi[i + 1] * new_u[i + 1] + eta[i + 1]

    return new_u


# ===========================================================================================================================

def simple_iterations_method_x(z, prev_u):
    u = prev_u
    for _ in range(100):
        new_u = right_hand_run_method_x(z, u, prev_u)

        repeat = False
        for i in range(Hx_COUNT):
            if abs((u[i] - new_u[i]) / new_u[i]) > EPS:
                repeat = True
                break

        u = new_u

        if not repeat:
            break

    return u


def simple_iterations_method_z(x, prev_u):
    u = prev_u
    for _ in range(100):
        new_u = right_hand_run_method_z(x, u, prev_u)

        repeat = False
        for i in range(Hz_COUNT):
            if abs((u[i] - new_u[i]) / new_u[i]) > EPS:
                repeat = True
                break

        u = new_u

        if not repeat:
            break

    if not new_u:
        print("new_u is None in simple_iterations_method_z")

    return u


def simple_iterations_method():
    prev_u = [[U0 for _ in range(Hx_COUNT)] for _ in range(Hz_COUNT)]
    cur_u = [[U0 for _ in range(Hx_COUNT)] for _ in range(Hz_COUNT)]

    flag = True

    count = 0

    while flag:
        for i in range(Hz_COUNT):
            new_row = simple_iterations_method_x(i * Hz, cur_u[i])
            cur_u[i] = new_row

        for i in range(Hx_COUNT):
            new_col = simple_iterations_method_z(i * Hx, [row[i] for row in cur_u])
            for j in range(Hz_COUNT):
                cur_u[j][i] = new_col[j]

        flag = False
        for i in range(Hz_COUNT):
            for j in range(Hx_COUNT):
                if abs(cur_u[i][j] - prev_u[i][j]) / TAU > EPS:
                    flag = True
                    break
            if flag:
                break

        prev_u = [row[:] for row in cur_u]
        count += 1

    print(count)
    return cur_u


# ===========================================================================================================================

def get_optimal_step_hx():
    global Hx_COUNT
    global Hx
    global Hz_COUNT
    global Hz
    global TAU

    Hx_COUNT = 3
    Hx = (x_max - x_min) / (Hx_COUNT - 1)

    Hz_COUNT = 3
    Hz = (z_max - z_min) / (Hz_COUNT - 1)

    TAU = 10

    tb = PrettyTable(['Hx', 'Hz', 'TAU'])

    u = simple_iterations_method()
    Hx /= 2
    Hx_COUNT = int(((x_max - x_min) / Hx) + 1)

    while Hx >= 0.0125:
        cur_u = simple_iterations_method()
        find = False

        for n in range(0, Hx_COUNT, 2):
            if abs((u[len(u) // 2][n // 2] - cur_u[len(cur_u) // 2][n]) / cur_u[len(cur_u) // 2][n]) > EPS:
                find = True
                break

        u = cur_u

        if not find:
            tb.add_row(["{:.6f}".format(Hx * 2), "{:.6f}".format(Hz), "{:.6f}".format(TAU)])
            break

        Hx /= 2
        Hx_COUNT = int(((x_max - x_min) / Hx) + 1)

    print(tb)


# ===========================================================================================================================

def main():
    x = [i for i in np.arange(x_min, x_max + Hx / 2, Hx)]
    z = [i for i in np.arange(z_min, z_max + Hz / 2, Hz)]

    #####################################################################

    # Задание 1 (3D):
    u = simple_iterations_method()

    x, y = np.meshgrid(x, z)

    z = np.array([np.array(T_m) for T_m in u])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, z, cmap='magma')

    ax.set_xlabel('x')
    ax.set_ylabel('z')
    ax.set_zlabel('u(x, z)')
    ax.set_title('Температурное поле')
    plt.show()

    # Задание 1 (по x):
    # u = simple_iterations_method()
    # fix_z = 99

    # plt.subplot(1, 1, 1)
    # plt.plot(x, [row[fix_z] for row in u], color, label=f"u(x) z={fix_z}")
    # plt.legend()
    # plt.title('u')
    # plt.grid()
    # plt.show()

    # Задание 1 (по z):
    # u = simple_iterations_method()
    # fix_x = 1

    # plt.subplot(1, 1, 1)
    # plt.plot(z, [row[fix_x] for row in u], color, label=f"u(x) z={fix_x}")
    # plt.legend()
    # plt.title('u')
    # plt.grid()
    # plt.show()

    #####################################################################
    # Задание 2.1:
    # get_optimal_step_hx()
    # get_optimal_step_hz()
    # get_optimal_step_tau()

    # Задание 2.2:
    # check_steps()


if __name__ == "__main__":
    main()
