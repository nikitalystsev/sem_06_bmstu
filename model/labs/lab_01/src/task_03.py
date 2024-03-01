import numpy as np
import matplotlib.pyplot as plt


def picard_method(x, n):
    u = np.zeros_like(x)
    u[0] = 0
    for i in range(1, n + 1):
        u = u + (x ** 2 + u ** 2) * (x[1] - x[0])
    return u


def euler_method(x, h):
    u = np.zeros_like(x)
    u[0] = 0
    for i in range(1, len(x)):
        u[i] = u[i - 1] + h * (x[i - 1] ** 2 + u[i - 1] ** 2)
    return u


# Определение интервала и шага
xmax = 3  # Примерное значение
step = 0.1

# Создание массива аргументов
x = np.arange(0, xmax + step, step)

# Решение методом Пикара
u_picard_1 = picard_method(x, 1)
u_picard_2 = picard_method(x, 2)
u_picard_3 = picard_method(x, 3)
u_picard_4 = picard_method(x, 4)

# Решение методом Эйлера
h = 0.01  # Начальный шаг
u_euler = euler_method(x, h)

# Вывод результатов
print("x\t\tPicard 1\tPicard 2\tPicard 3\tPicard 4\tEuler")
for i in range(len(x)):
    print(
        f"{x[i]:.2f}\t\t{u_picard_1[i]:.6f}\t{u_picard_2[i]:.6f}\t{u_picard_3[i]:.6f}\t{u_picard_4[i]:.6f}\t{u_euler[i]:.6f}")

# Визуализация
plt.plot(x, u_picard_1, label="Picard 1")
plt.plot(x, u_picard_2, label="Picard 2")
plt.plot(x, u_picard_3, label="Picard 3")
plt.plot(x, u_picard_4, label="Picard 4")
plt.plot(x, u_euler, label="Euler")
plt.xlabel("x")
plt.ylabel("u(x)")
plt.title("Solutions using Picard and Euler methods")
plt.legend()
plt.grid(True)
plt.show()
