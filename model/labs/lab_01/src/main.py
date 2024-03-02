import task_01
import task_02
import task_03

import numpy as np
import matplotlib.pyplot as plt


def print_menu() -> None:
    """
    Функция вывода меню
    """
    print(
        """
        1. Задача №1;
        2. Задача №2;
        3. Задача №3;
        0. Выход из программы.
        """
    )


def main() -> None:
    """
    Главная функция
    """

    while True:
        print_menu()

        try:
            menu_item = int(input("Выберите пункт меню: "))
        except ValueError:
            print("Неверный пункт меню! Попробуйте еще раз")
            continue

        match menu_item:
            case 1:
                task_01.get_solution()
            case 2:
                task_02.get_solution()
            case 3:
                task_03.get_solution()
            case 0:
                exit(0)
            case _:
                print("Неверный пункт меню! Попробуйте еще раз")


if __name__ == '__main__':
    main()
