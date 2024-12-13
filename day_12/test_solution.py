from solution import parse_input, part_1, part_2


def test_parse_input():
    matrix = parse_input()
    assert len(matrix) == len(matrix[0]) == 140


def test_part1():
    matrix = parse_input()
    assert part_1(matrix) == 1319878


def test_part2():
    matrix = parse_input()
    assert part_2(matrix) == 784982
