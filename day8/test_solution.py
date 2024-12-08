from solution import parse_input, part_1, part_2


def test_parse_input():
    matrix, nodes = parse_input()
    assert len(matrix[0]) == 50
    assert len(matrix) == 50
    assert len(nodes) == 44


def test_part1():
    matrix, nodes = parse_input()
    assert part_1(matrix=matrix, nodes=nodes) == 273


def test_part2():
    matrix, nodes = parse_input()
    assert part_2(matrix=matrix, nodes=nodes) == 1017
