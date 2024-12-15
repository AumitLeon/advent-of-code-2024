from solution import (
    parse_input,
    part_1,
    part_2_minimize_entropy,
    ROW_DIMENSION,
    COLUMN_DIMENSION,
)


def test_parse_input():
    robots = parse_input()
    assert len(robots) == 500


def test_part_1():
    robots = parse_input()
    assert (
        part_1(
            robots=robots, row_dimension=ROW_DIMENSION, col_dimension=COLUMN_DIMENSION
        )
        == 229980828
    )


def test_part_2_minimize_entropy():
    robots = parse_input()
    assert (
        part_2_minimize_entropy(
            robots=robots,
            row_dimension=ROW_DIMENSION,
            col_dimension=COLUMN_DIMENSION,
            iterations=10000,
        )
        == 7132
    )
