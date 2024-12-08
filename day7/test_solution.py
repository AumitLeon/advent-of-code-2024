from solution import parse_input, part_1, part_2


def test_parse_input():
    operations = parse_input()
    assert len(operations) == 850


def test_part1():
    operations = parse_input()
    assert part_1(operations) == 1985268524462


def test_part2():
    operations = parse_input()
    assert part_2(operations) == 150077710195188
