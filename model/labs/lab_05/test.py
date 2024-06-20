from math import exp
import numpy as np
from matplotlib import pyplot as plt

u0 = 300
x_max = 10
K, N = 0, 0
EPS = 1e-3


def f(f0, beta, x0, z0, x, z):
    return f0 * exp(-beta * ((x - x0) ** 2 * (z - z0) ** 2))


def lambd(a1, b1, c1, m1, u):
    # return a1 * (b1 + c1 * u**m1)
    return 0.16


def rightX(u0):
    KN = 0
    MN = 1
    PN = u0
    return KN, MN, PN


def leftX(u0):
    K0 = 1
    M0 = 0
    P0 = u0
    return K0, M0, P0


def progonka_x(k, tau, hx, hz, prevLayer, f0, beta, x0, z0):
    global N
    K0, M0, P0 = leftX(u0)
    KN, MN, PN = rightX(u0)

    A = [1 / hx ** 2 for _ in range(N)]
    B = [-1 / (0.5 * tau) - 2 / hx ** 2 for _ in range(N)]
    C = [1 / hx ** 2 for _ in range(N)]
    F = [0 for _ in range(N)]

    for i in range(len(F)):
        # print('repv_layer[i][k] / (0.5*tau)', prevLayer[i][k] / (0.5 * tau))
        # print('div', (prevLayer[i][k-1] - 2 * prevLayer[i][k] + prevLayer[i][k+1]) / hz**2)
        # print('f', f(f0, beta, x0, z0, hx*i, hz*k) / lambd(1, 2, 3, 4, 5))
        # print(prevLayer[i][k-1], prevLayer[i][k], prevLayer[i][k+1])
        F[i] = -(prevLayer[i][k] / (0.5 * tau) + \
                 (prevLayer[i][k - 1] - 2 * prevLayer[i][k] + prevLayer[i][k + 1]) / hz ** 2 + \
                 f(f0, beta, x0, z0, hx * i, hz * k) / lambd(1, 2, 3, 4, 5))

    # print('F', F)

    xi = [0, -M0 / K0]
    eta = [0, P0 / K0]
    # print('xi', xi, 'eta', eta)

    x = hx
    n = 1

    # Прямой ход
    while x < x_max - hx / 2:
        cur_xi = -C[n] / (B[n] + A[n] * xi[n])
        cur_eta = (F[n] - A[n] * eta[n]) / (B[n] + A[n] * xi[n])
        # print('cur xi eta', cur_xi, cur_eta)
        xi.append(cur_xi)
        eta.append(cur_eta)
        n += 1
        x += hx

    n += 1
    # Обратный ход
    new_u = [0] * (n)
    new_u[n - 1] = (PN - KN * eta[n - 1]) / (MN + KN * xi[n - 1])
    # print('x', new_u[n-1])
    for i in range(n - 2, -1, -1):
        new_u[i] = xi[i + 1] * new_u[i + 1] + eta[i + 1]
    return new_u


def leftZ(u0):
    K0 = 1
    M0 = 0
    P0 = u0
    return K0, M0, P0


def rightZ(u0):
    KN = 0
    MN = 1
    PN = u0
    return KN, MN, PN


def progonka_z(n, tau, hx, hz, curLayer, f0, beta, x0, z0):
    global K
    K0, M0, P0 = leftX(u0)
    KN, MN, PN = rightX(u0)

    A = [1 / hz ** 2 for _ in range(K)]
    B = [-1 / (0.5 * tau) - 2 / hz ** 2 for _ in range(K)]
    C = [1 / hz ** 2 for _ in range(K)]
    F = [0 for _ in range(K)]

    for i in range(K):
        F[i] = -(curLayer[n][i] / (0.5 * tau) + \
                 (curLayer[n - 1][i] - 2 * curLayer[n][i] + curLayer[n + 1][i]) / hz ** 2 + \
                 f(f0, beta, x0, z0, hx * n, hz * i) / lambd(1, 2, 3, 4, 5))
    # print('Fz', F)

    xi = [0, -M0 / K0]
    eta = [0, P0 / K0]

    x = hx
    n = 1

    # Прямой ход
    while x < x_max - hx / 2:
        xi.append(-C[n] / (B[n] + A[n] * xi[n]))
        eta.append((F[n] - A[n] * eta[n]) / (B[n] + A[n] * xi[n]))
        n += 1
        x += hx

    n += 1
    # Обратный ход
    new_u = [0] * (n)
    new_u[n - 1] = (PN - KN * eta[n - 1]) / (MN + KN * xi[n - 1])
    # print('z', new_u[n-1])
    for i in range(n - 2, -1, -1):
        new_u[i] = xi[i + 1] * new_u[i + 1] + eta[i + 1]
    return new_u


def stop_criteria(prev_layer, cur_layer, t, eps):
    is_stop = True

    for i in range(len(prev_layer)):
        for j in range(len(prev_layer[0])):
            # print(cur_layer)
            # print(prev_layer)
            # print(abs((cur_layer[i][j] - prev_layer[i][j]) / prev_layer[i][j]))
            # print('ff', cur_layer[i][j], prev_layer[i][j])
            # print(cur_layer[i][j] - prev_layer[i][j] / prev_layer[i][j])
            if abs((cur_layer[i][j] - prev_layer[i][j]) / prev_layer[i][j]) >= eps:
                is_stop = False
                return is_stop
    # print("good")
    return is_stop


def transpose(matrix):
    trans_matrix = [[0 for j in range(len(matrix))] for i in range(len(matrix[0]))]
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            trans_matrix[j][i] = matrix[i][j]

    return trans_matrix


def solve(params: dict, prevLayer):
    global K, N
    N = int(params['a'] / params['hx'])
    K = int(params['b'] / params['hz'])
    T = int(params['tmax'] / params['tau'])

    u_x = []
    for k in range(1, K - 1):
        u_x.append(
            progonka_x(k,
                       params['tau'],
                       params['hx'],
                       params['hz'],
                       prevLayer,
                       params['f0'],
                       params['beta'],
                       params['x0'],
                       params['z0']
                       )
        )
    u_x = [[params['u0'] for i in range(N)]] + u_x + [[params['u0'] for i in range(N)]]
    # print(u_x)
    # print(len(u_x), len(u_x[0]))

    cur_u = []
    for n in range(1, N - 1):
        cur_u.append(
            progonka_z(
                n,
                params['tau'],
                params['hx'],
                params['hz'],
                transpose(u_x),
                params['f0'],
                params['beta'],
                params['x0'],
                params['z0']
            )
        )

    cur_u = [[params['u0'] for i in range(N)]] + cur_u + [[params['u0'] for i in range(N)]]
    # print('cur_u', cur_u)

    return transpose(cur_u)
    # return cur_u


def iterations(params, debug):
    global K, N
    N = int(params['a'] / params['hx'])
    K = int(params['b'] / params['hz'])

    pr = [[params['u0']] * N for _ in range(K)]

    cur = solve(params, pr)
    i = 0
    while not stop_criteria(pr, cur, params['tau'], EPS):
        pr = cur
        cur = solve(params, pr)
        i += 1
        if debug:
            print(f"DFGZFDGFSDGFDBTBGEFRFEREFi = {i=}")
        # if i > 1:
        # break
        # break

    return cur


def iterations_times(params, time, debug):
    global K, N
    N = int(params['a'] / params['hx'])
    K = int(params['b'] / params['hz'])

    pr = [[params['u0']] * N for _ in range(K)]

    cur = solve(params, pr)
    i = 0
    while not stop_criteria(pr, cur, params['tau'], EPS):
        pr = cur
        cur = solve(params, pr)
        i += 1
        if debug:
            print(f"{i=}")
        if i > time:
            return None

    return cur


def optSteps(params, maxIter):
    start_x, start_z, start_tau = 0.1, 0.1, 1
    params['hx'], params['hz'], params['tau'] = start_x, start_z, start_tau
    flag = True
    while flag:
        ans = iterations_times(params, maxIter, False)
        if ans != []:
            params['hx'] *= 2
            params['hz'] *= 2
            params['tau'] *= 2
            print(params['hx'])
            print(ans)
        else:
            break
    print("first bad step x = ", params['hx'])


if __name__ == '__main__':
    params = {
        'u0': 300,
        'f0': 1,
        'x0': 3,
        'z0': 3,
        'beta': 1,
        'hx': 0.1,
        'hz': 0.1,
        'tau': 1,
        'a': 10,
        'b': 10,
        'tmax': 10
    }

    ans = iterations(params, True)
    x = np.linspace(0, params['a'], len(ans[0]))
    z = np.linspace(0, params['b'], len(ans))

    X, Y = np.meshgrid(x, z)

    farr = np.array([np.array(T_m) for T_m in ans])
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X, Y, farr, cmap="viridis")

    ax.set_xlabel("x")
    ax.set_ylabel("z")
    ax.set_zlabel("U(x, z)")
    plt.show()

    plt.imshow(ans, cmap='viridis')
    plt.colorbar()
    plt.show()

    # fig, axs = plt.subplots(2, 2)  # Создаем сетку из 2 строк и 2 столбцов поддиаграмм
    # times = [1, 5, 7, 9]

    # for i in range(len(times)):
    #     ans = iterations_times(params, times[i], False)
    #     axs[i // 2, i % 2].imshow(ans, cmap='viridis')  # Отображение графика в соответствующей поддиаграмме
    #     # axs[i // 2, i % 2].colorbar()  # Добавление цветовой шкалы к поддиаграмме

    # plt.show()

    # # одномерные графики при фикс x
    # for i in range(N):
    #     if i % 10 == 0:
    #         u_z = ans[i]
    #         plt.plot(z, u_z, label="x = {}".format(i//10))
    #         plt.xlabel("z")
    #         plt.ylabel("u")
    #         plt.legend()
    # plt.show()

    # # одномерные графики при фикс z
    # for i in range(K):
    #     if i % 10 == 0:
    #         u_x = []
    #         for j in range(N):
    #             u_x.append(ans[j][i])
    #         plt.plot(x, u_x, label="z = {}".format(i//10))
    #         plt.xlabel("x")
    #         plt.ylabel("u")
    #         plt.legend()   
    # plt.show()     

    # шаги
    optSteps(params, 100)




