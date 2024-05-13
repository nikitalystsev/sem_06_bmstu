import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Ваша двумерная матрица значений функции
Z = np.random.rand(10, 10)  # Пример случайных значений, замените на вашу матрицу

# Создание сетки x и y
x = np.arange(Z.shape[0])
y = np.arange(Z.shape[1])
X, Y = np.meshgrid(x, y)

# Построение графика
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis')

# Настройка подписей осей
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Трехмерный график функции от двух переменных')

# Показать график
plt.show()
