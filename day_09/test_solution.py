from solution import parse_input, part1, part2, construct_disk_map, create_tuples


def test_parse_input():
    input = parse_input()
    assert len(input) == 19999


def test_part1():
    input = parse_input()
    parsed_input = create_tuples(input)
    disk_map = construct_disk_map(parsed_input)
    assert part1(disk_map=disk_map) == 6398608069280


def test_part2():
    input = parse_input()
    parsed_input = create_tuples(input)
    assert part2(tuples=parsed_input) == 6427437134372
