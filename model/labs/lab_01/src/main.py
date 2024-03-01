import task_01

import numpy as np
import matplotlib.pyplot as plt


def main() -> None:
    """
    Главная функция
    """

    f_row = task_01.get_u_x_by_row(0)
    f_euler = task_01.get_u_x_by_euler()
    f_picard1 = task_01.get_u_x_by_picard1()
    f_picard2 = task_01.get_u_x_by_picard2()

    x_values: np.ndarray | tuple[np.ndarray, float | None] = np.linspace(-2, 6, 100)
    y_values_picard2: np.ndarray | tuple[np.ndarray, float | None] = f_picard2(x_values)
    y_values_row: np.ndarray | tuple[np.ndarray, float | None] = f_row(x_values)

    x_min = min(x_values)
    x_max = max(x_values)
    y_min = min(min(y_values_picard2), min(y_values_row))
    y_max = max(max(y_values_picard2), max(y_values_row))

    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))

    # Постройте первый график
    axs[0].plot(x_values, y_values_picard2, color='blue')
    axs[0].set_title('Метод Пикара (2-е приближение)')
    axs[0].set_xlim(x_min, x_max)
    axs[0].set_ylim(y_min, y_max)
    axs[0].grid(True)

    # Постройте второй график
    axs[1].plot(x_values, y_values_row, color='red')
    axs[1].set_title('Разложение в ряд Тейлора (первые 5 членов)')
    axs[1].set_xlim(x_min, x_max)
    axs[1].set_ylim(y_min, y_max)
    axs[1].grid(True)

    # Отобразите все графики
    plt.tight_layout()  # Распределить графики равномерно по окну
    plt.show()

    print(f_row(0.1))
    print(f_euler(0.1))
    print(f_picard1(0.1))
    print(f_picard2(0.1))


if __name__ == '__main__':
    main()
