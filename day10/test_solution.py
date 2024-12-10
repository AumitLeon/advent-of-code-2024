from solution import parse_input, count_trails, count_ratings


def test_parse_input():
    matrix, trail_starts = parse_input()
    assert len(matrix) == len(matrix[0]) == 55
    assert len(trail_starts) == 297


def test_part1_count_trails():
    matrix, trail_starts = parse_input()
    assert count_trails(matrix=matrix, trail_starts=trail_starts) == 825


def test_part1_count_ratings():
    matrix, trail_starts = parse_input()
    assert count_ratings(matrix=matrix, trail_starts=trail_starts) == 1805
