from solution import parse_input, multiply, multiply_part2


def test_parse_input():
    assert len(parse_input()) == 6


def test_multiply():
    parsed_input = parse_input()
    assert multiply(parsed_input) == 173419328


def test_multiply_part2():
    parsed_input = parse_input()
    assert multiply_part2(parsed_input) == 90669332
