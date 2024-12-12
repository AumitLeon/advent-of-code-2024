from solution import parse_input, solution_part1, solution_part2


def test_parse_input():
    matrix = parse_input()
    assert len(matrix) == 140 and len(matrix[1]) == 140


def test_solution_part1():
    matrix = parse_input()
    assert solution_part1(matrix) == 2642


def test_solution_part2():
    matrix = parse_input()
    assert solution_part2(matrix) == 1974
