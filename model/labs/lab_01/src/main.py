import task_01


def main() -> None:
    """
    Главная функция
    """

    f_row = task_01.get_u_x_by_row(0)
    f_euler = task_01.get_u_x_by_euler()
    f_picard = task_01.get_u_x_by_picard()

    print(f_row(0.1))
    print(f_euler(0.1))
    print(f_picard(0.1))


if __name__ == '__main__':
    main()
