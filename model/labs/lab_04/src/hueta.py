# def left_sweep(t_m, curr_time, data: Grid, ops: TaskOps):
#     """
#     Реализация левой прогонки
#     """
#
#     b, h, tau = data.b, data.h, data.tau
#     # Прямой ход
#     k_0, m_0, p_0 = left_boundary_condition(t_m, curr_time, data, ops)
#     k_n, m_n, p_n = right_boundary_condition(t_m, curr_time, data, ops)
#
#     ksi = [-k_n / m_n, 0]
#     eta = [p_n / m_n, 0]
#
#     x = b - h
#     n = -2
#     cnt = 1
#
#     for i in range(len(t_m) - 2, 0, -1):
#         a_n = kappa(t_m[i - 1], t_m[i], ops) * tau / h
#         d_n = kappa(t_m[i], t_m[i + 1], ops) * tau / h
#         b_n = a_n + d_n + _c(t_m[i], ops) * h + p(x, ops) * h * tau
#         f_n = _c(t_m[i], ops) * t_m[i] * h + f(x, curr_time, t_m[i], ops) * h * tau
#
#         ksi.insert(0, a_n / (b_n - d_n * ksi[n]))
#         eta.insert(0, (d_n * eta[n] + f_n) / (b_n - d_n * ksi[n]))
#
#         n -= 1
#         x -= h
#         cnt += 1
#
#     # Обратный ход
#     u = [0] * (cnt + 1)
#
#     u[0] = (p_0 - k_0 * eta[0]) / (m_0 + k_0 * ksi[0])
#
#     for i in range(1, cnt + 1):
#         u[i] = ksi[i - 1] * u[i - 1] + eta[i - 1]
#
#     return u
#
#
# def meetings_sweep(t_m, curr_time, data: Grid, ops: TaskOps, n_eq):
#     """
#     Реализация встречной прогонки
#     """
#     b, h, tau = data.b, data.h, data.tau
#
#     # Прямой ход
#     k_0, m_0, p_0 = left_boundary_condition(t_m, curr_time, data, ops)
#     k_n, m_n, p_n = right_boundary_condition(t_m, curr_time, data, ops)
#
#     # правая часть прогонки
#     x = h
#     n = 1
#
#     ksi_r = [0, -k_0 / m_0]
#     eta_r = [0, p_0 / m_0]
#
#     for i in range(1, n_eq):
#         a_n = kappa(t_m[i - 1], t_m[i], ops) * tau / h
#         d_n = kappa(t_m[i], t_m[i + 1], ops) * tau / h
#         b_n = a_n + d_n + _c(t_m[i], ops) * h + p(x, ops) * h * tau
#         f_n = _c(t_m[i], ops) * t_m[i] * h + f(x, curr_time, t_m[i], ops) * h * tau
#
#         ksi_r.append(d_n / (b_n - a_n * ksi_r[n]))
#         eta_r.append((a_n * eta_r[n] + f_n) / (b_n - a_n * ksi_r[n]))
#
#         n += 1
#         x += h
#
#     # левая часть прогонки
#     ksi_l = [-k_n / m_n, 0]
#     eta_l = [p_n / m_n, 0]
#
#     x = b - h
#     n1 = -2
#     cnt = 1
#
#     for i in range(len(t_m) - 2, n_eq - 1, -1):
#         a_n = kappa(t_m[i - 1], t_m[i], ops) * tau / h
#         d_n = kappa(t_m[i], t_m[i + 1], ops) * tau / h
#         b_n = a_n + d_n + _c(t_m[i], ops) * h + p(x, ops) * h * tau
#         f_n = _c(t_m[i], ops) * t_m[i] * h + f(x, curr_time, t_m[i], ops) * h * tau
#
#         ksi_l.insert(0, a_n / (b_n - d_n * ksi_l[n1]))
#         eta_l.insert(0, (d_n * eta_l[n1] + f_n) / (b_n - d_n * ksi_l[n1]))
#
#         n1 -= 1
#         x -= h
#         cnt += 1
#
#     # # Обратный ход
#     u = [0] * (n + cnt)
#
#     # вычисляем up (решая систему из двух уравнений) -- сопряжение решений
#     u[n_eq] = (ksi_r[-1] * eta_l[0] + eta_r[-1]) / (1 - ksi_r[-1] * ksi_l[0])
#
#     for i in range(n_eq - 1, -1, -1):
#         u[i] = ksi_r[i + 1] * u[i + 1] + eta_r[i + 1]
#
#     for i in range(n_eq + 1, n + cnt):
#         _i = i - n_eq
#         u[i] = ksi_l[_i - 1] * u[i - 1] + eta_l[_i - 1]
#
#     return u