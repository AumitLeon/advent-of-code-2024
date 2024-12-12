from solution import parse_input, part_1, part_2


def test_parse_input():
    stones = parse_input()
    assert len(stones) == 8


def test_part1():
    stones = parse_input()
    assert part_1(stones) == 190865


def test_part2():
    stones = parse_input()
    assert part_2(stones) == 225404711855335
