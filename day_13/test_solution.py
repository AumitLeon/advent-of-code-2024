from solution import parse_input, solve_system_of_equations


def test_parse_input():
    equations = parse_input(part=1)
    assert len(equations) == 320
    assert all([len(eq) == 3 for eq in equations])
    # assert len(trail_starts) == 297


def test_solve_system_of_equations_part1():
    equations = parse_input(part=1)
    assert solve_system_of_equations(equations=equations) == 26299


def test_solve_system_of_equations_part2():
    equations = parse_input(part=2)
    assert solve_system_of_equations(equations=equations) == 107824497933339.0
