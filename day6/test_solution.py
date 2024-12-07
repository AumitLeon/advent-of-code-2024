from solution import parse_input, count_visited, find_possible_loops


def test_parse_input():
    matrix, starting_coords = parse_input()
    assert len(matrix) == 130 and len(matrix[1]) == 130
    assert starting_coords == (60, 36)


def test_count_visited():
    matrix, starting_coords = parse_input()
    assert (
        count_visited(matrix=matrix, coords=starting_coords, orientation="NORTH")
        == 4789
    )


def test_find_possible_loops():
    matrix, starting_coords = parse_input()
    assert len(find_possible_loops(matrix=matrix, coords=starting_coords)) == 1304
