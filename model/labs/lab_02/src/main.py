from solution_system import SolutionSystemByShootingMethod


def main() -> None:
    """
    Главная функция
    """

    # какая-то логика
    ex = SolutionSystemByShootingMethod()
    # ex.print_solve(ex.get_solve_by_rk_2, "../data/cmp_rk2_rk4.png")

    # ex.print_solve(ex.get_solve_by_rk_2, "rk2")
    ex.print_solve(ex.get_solve_by_rk_4, "rk4")

    # ex.cmp_rk2_rk4()
    # ex.get_solve_by_auto_step_sel()


if __name__ == '__main__':
    main()
