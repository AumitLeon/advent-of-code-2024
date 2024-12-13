from typing import List, Tuple
from copy import deepcopy


def parse_input() -> List[List[str]]:
    matrix = []
    with open("input.txt") as file:
        for line in file:
            row = line.rstrip()
            processed_row = [c.rstrip() for c in row]
            matrix.append(processed_row)

    return matrix


def get_possible_positions(row_idx: int, column_idx: int) -> List[Tuple[int, int]]:
    return [
        (row_idx + 1, column_idx),  # Below
        (row_idx - 1, column_idx),  # Above
        (row_idx, column_idx + 1),  # Right
        (row_idx, column_idx - 1),  # Left
    ]


def mark_visited(matrix: List[List[str]], coords: Tuple[int, int], current_char: str):
    row, col = coords
    matrix[row][col] = current_char.lower()


def is_valid_position(
    matrix: List[List[str]], coords: Tuple[int, int], current_char: str
) -> bool:
    row, col = coords
    matrix_col_dimension = len(matrix[0])
    matrix_row_dimension = len(matrix)
    if (
        0 > col
        or col > matrix_col_dimension - 1
        or 0 > row
        or row > matrix_row_dimension - 1
        or matrix[row][col] != current_char
    ):
        return False
    else:
        return True


def is_edge(matrix: List[List[str]], coords: Tuple[int, int]) -> bool:
    row, col = coords
    matrix_col_dimension = len(matrix[0])
    matrix_row_dimension = len(matrix)
    if (
        0 > col
        or col > matrix_col_dimension - 1
        or 0 > row
        or row > matrix_row_dimension - 1
    ):
        return True
    else:
        return False


def traverse_plots(
    start_coords: Tuple[int, int], matrix: List[List[str]], current_char: str
):
    start_row, start_col = start_coords
    mark_visited(matrix, (start_row, start_col), current_char)
    visited = 1
    touched = 0

    possible_positions = get_possible_positions(start_row, start_col)

    for pos in possible_positions:
        next_row, next_col = pos
        if is_valid_position(matrix, pos, current_char):
            # Traverse the path
            traversal_visited, traveral_touched = traverse_plots(
                start_coords=pos, matrix=matrix, current_char=current_char
            )
            visited += traversal_visited
            touched += traveral_touched
        else:
            if (
                is_edge(matrix, pos)
                or matrix[next_row][next_col] != current_char.lower()
            ):
                touched += 1
    return visited, touched


def get_diaganols(row_idx: int, column_idx: int) -> List[Tuple[int, int]]:
    return [
        (row_idx - 1, column_idx - 1),  # Top left
        (row_idx - 1, column_idx + 1),  # Top right
        (row_idx + 1, column_idx + 1),  # Bottom right
        (row_idx + 1, column_idx - 1),  # Bottom left
    ]


def safe_get_matrix_position(matrix: List[List[str]], coords: Tuple[int, int]):
    row, col = coords
    if is_edge(matrix, coords):
        return "."
    else:
        return matrix[row][col]


def count_corners(
    matrix: List[List[str]],
    possible_positions: List[Tuple[int, int]],
    current_char: str,
    diagonals: List[Tuple[int, int]],
):
    corners = 0

    matrix_left = safe_get_matrix_position(matrix, possible_positions[3])
    matrix_right = safe_get_matrix_position(matrix, possible_positions[2])
    matrix_above = safe_get_matrix_position(matrix, possible_positions[1])
    matrix_below = safe_get_matrix_position(matrix, possible_positions[0])

    matrix_above_left = safe_get_matrix_position(matrix, diagonals[0])
    matrix_above_right = safe_get_matrix_position(matrix, diagonals[1])
    matrix_below_right = safe_get_matrix_position(matrix, diagonals[2])
    matrix_below_left = safe_get_matrix_position(matrix, diagonals[3])

    # Concave Top left corner
    if (
        matrix_left.lower() != current_char.lower()
        and matrix_above.lower() != current_char.lower()
    ):
        corners += 1
    # Convex top left corner
    if (
        matrix_right.lower() == current_char.lower()
        and matrix_below.lower() == current_char.lower()
        and matrix_below_right.lower() != current_char.lower()
    ):
        corners += 1
    # Convex Top right corner
    if (
        matrix_left.lower() == current_char.lower()
        and matrix_below.lower() == current_char.lower()
        and matrix_below_left.lower() != current_char.lower()
    ):
        corners += 1
    # Concave Top right corner
    if (
        matrix_right.lower() != current_char.lower()
        and matrix_above.lower() != current_char.lower()
    ):
        corners += 1
    # Convex Bottom right corner
    if (
        matrix_left.lower() == current_char.lower()
        and matrix_above.lower() == current_char.lower()
        and matrix_above_left.lower() != current_char.lower()
    ):
        corners += 1
    # Concave Bottom right corner
    if (
        matrix_right.lower() != current_char.lower()
        and matrix_below.lower() != current_char.lower()
    ):
        corners += 1
    # Convex Bottom left corner
    if (
        matrix_right.lower() == current_char.lower()
        and matrix_above.lower() == current_char.lower()
        and matrix_above_right.lower() != current_char.lower()
    ):
        corners += 1
    # Concave Bottom left corner
    if (
        matrix_left.lower() != current_char.lower()
        and matrix_below.lower() != current_char.lower()
    ):
        corners += 1

    return corners


def traverse_plots_part_2(
    start_coords: Tuple[int, int], matrix: List[List[str]], current_char: str
):
    start_row, start_col = start_coords
    mark_visited(matrix, (start_row, start_col), current_char)
    visited = 1

    possible_positions = get_possible_positions(start_row, start_col)
    diagonals = get_diaganols(start_row, start_col)
    corners = count_corners(matrix, possible_positions, current_char, diagonals)
    for pos in possible_positions:
        if is_valid_position(matrix, pos, current_char):
            # Traverse the path
            traversal_visited, traveral_touched = traverse_plots_part_2(
                start_coords=pos, matrix=matrix, current_char=current_char
            )
            visited += traversal_visited
            corners += traveral_touched

    return visited, corners


def print_matrix(matrix: List[List[str]]):
    for row in matrix:
        print("".join(row))


def part_1(matrix: List[List[str]]) -> int:
    price = 0
    for row_idx, row in enumerate(matrix):
        for col_idx, _ in enumerate(row):
            if matrix[row_idx][col_idx].isupper():
                # Do a DFS.
                visited, touched = traverse_plots(
                    start_coords=(row_idx, col_idx),
                    matrix=matrix,
                    current_char=matrix[row_idx][col_idx],
                )
                price += visited * touched
    return price


def part_2(matrix: List[List[str]]) -> int:
    price = 0
    for row_idx, row in enumerate(matrix):
        for col_idx, _ in enumerate(row):
            if matrix[row_idx][col_idx].isupper():
                # Do a DFS.
                visited, corners = traverse_plots_part_2(
                    start_coords=(row_idx, col_idx),
                    matrix=matrix,
                    current_char=matrix[row_idx][col_idx],
                )
                price += visited * corners
    return price


if __name__ == "__main__":
    matrix = parse_input()
    matrix_part2 = deepcopy(matrix)

    result_part1 = part_1(matrix)
    print(f"Solution part 1: {result_part1}")

    result_part2 = part_2(matrix_part2)
    print(f"Solution part 2: {result_part2}")
