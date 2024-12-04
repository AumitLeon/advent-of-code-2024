from typing import List, Tuple


def get_possible_positions(row_idx: int, column_idx: int) -> List[Tuple[int, int]]:
    return [
        (row_idx + 1, column_idx),  # Below
        (row_idx - 1, column_idx),  # Above
        (row_idx, column_idx + 1),  # Right
        (row_idx, column_idx - 1),  # Left
        (row_idx - 1, column_idx - 1),  # Top left
        (row_idx - 1, column_idx + 1),  # Top right
        (row_idx + 1, column_idx + 1),  # Bottom right
        (row_idx + 1, column_idx - 1),  # Bottom left
    ]


def parse_input() -> List[List[str]]:
    lines = []
    with open("input.txt") as file:
        for line in file:
            row = line.rstrip()
            processed_row = [c if c in ("X", "M", "A", "S") else "." for c in row]
            lines.append(processed_row)
    return lines


def search_neighbors(
    next_char: str,
    matrix: List[List[str]],
    possible_positions: List[Tuple[int, int]],
    idx_of_possible_position: int = None,
) -> int:
    result = 0
    matrix_x_dimension = len(matrix)
    matrix_y_dimension = len(matrix[0])
    for idx, coordinates in enumerate(possible_positions):
        x, y = coordinates
        # Base cases
        if 0 > x or x > matrix_x_dimension - 1 or 0 > y or y > matrix_y_dimension - 1:
            continue

        if next_char == "M":
            if matrix[x][y] == "M":
                # It's possible we can go in multiple directions, so we should increment result
                result += search_neighbors(
                    next_char="A",
                    matrix=matrix,
                    # The only possible position to check in the next iteration is the direction that the "M" was found.
                    # I.e., if "M" was found going to the top right diagnoal position, the next iteration can only search for "A" by checking the top right diagonal position.
                    possible_positions=[get_possible_positions(x, y)[idx]],
                    # Propogate the only position in the list of possible positions that subsequent recursive calls can check.
                    # The index from the list of possible positions consistently reflects the same possible position.
                    # I.e., index 0 always corresponds to the position directly below the current position.
                    idx_of_possible_position=idx,
                )
            else:
                continue
        elif next_char == "A":
            if matrix[x][y] == "A":
                # Once at A, we can only move in the direction that we moved from the previous M, so we can return here,
                # since the next value will be 0 or 1 depending on if it's an S.
                return search_neighbors(
                    next_char="S",
                    matrix=matrix,
                    possible_positions=[
                        get_possible_positions(x, y)[idx_of_possible_position]
                    ],
                    idx_of_possible_position=idx_of_possible_position,
                )
            else:
                continue
        elif next_char == "S":
            # End our recursion if the last value is an S. We could only get here following a direct XMAS path.
            if matrix[x][y] == "S":
                return 1
            else:
                continue
        else:
            return 0
    return result


def solution_part1(matrix: List[List[str]]) -> int:
    counter = 0
    # Search the 8 possible positions.
    for row_idx, row in enumerate(matrix):
        for column_idx, column in enumerate(row):
            possible_positions = get_possible_positions(
                row_idx=row_idx, column_idx=column_idx
            )
            if column == "X":
                counter += search_neighbors(
                    next_char="M", matrix=matrix, possible_positions=possible_positions
                )
    return counter


def get_possible_positions_2(row_idx: int, column_idx: int) -> List[Tuple[int, int]]:
    # Only corners
    return [
        (row_idx - 1, column_idx - 1),  # Top left
        (row_idx - 1, column_idx + 1),  # Top right
        (row_idx + 1, column_idx - 1),  # Bottom left
        (row_idx + 1, column_idx + 1),  # Bottom right
    ]


def search_neighbors_part2(
    matrix: List[List[str]],
    possible_positions: List[Tuple[int, int]],
) -> int:
    matrix_x_dimension = len(matrix)
    matrix_y_dimension = len(matrix[0])

    for x, y in possible_positions:
        if 0 > x or x > matrix_x_dimension - 1 or 0 > y or y > matrix_y_dimension - 1:
            return 0
    # Top left corner
    # M . M
    # . A .
    # S . S
    if (
        matrix[possible_positions[0][0]][possible_positions[0][1]] == "M"
        and matrix[possible_positions[3][0]][possible_positions[3][1]] == "S"
        and matrix[possible_positions[1][0]][possible_positions[1][1]] == "M"
        and matrix[possible_positions[2][0]][possible_positions[2][1]] == "S"
    ):
        return 1
    # Top left corner
    # S . S
    # . A .
    # M . M
    elif (
        matrix[possible_positions[0][0]][possible_positions[0][1]] == "S"
        and matrix[possible_positions[3][0]][possible_positions[3][1]] == "M"
        and matrix[possible_positions[1][0]][possible_positions[1][1]] == "S"
        and matrix[possible_positions[2][0]][possible_positions[2][1]] == "M"
    ):
        return 1
    # Top left corner
    # M . S
    # . A .
    # M . S
    elif (
        matrix[possible_positions[0][0]][possible_positions[0][1]] == "M"
        and matrix[possible_positions[3][0]][possible_positions[3][1]] == "S"
        and matrix[possible_positions[1][0]][possible_positions[1][1]] == "S"
        and matrix[possible_positions[2][0]][possible_positions[2][1]] == "M"
    ):
        return 1
    # Top left corner
    # S . M
    # . A .
    # S . M
    elif (
        matrix[possible_positions[0][0]][possible_positions[0][1]] == "S"
        and matrix[possible_positions[3][0]][possible_positions[3][1]] == "M"
        and matrix[possible_positions[1][0]][possible_positions[1][1]] == "M"
        and matrix[possible_positions[2][0]][possible_positions[2][1]] == "S"
    ):
        return 1
    else:
        return 0


def solution_part2(matrix: List[List[str]]):
    counter = 0
    # Search the 8 possible positions.
    for row_idx, row in enumerate(matrix):
        for column_idx, column in enumerate(row):
            possible_positions = get_possible_positions_2(
                row_idx=row_idx, column_idx=column_idx
            )
            if column == "A":
                counter += search_neighbors_part2(
                    matrix=matrix, possible_positions=possible_positions
                )
    return counter


if __name__ == "__main__":
    input = parse_input()
    result_part1 = solution_part1(input)
    print(f"Solution to part 1: {result_part1}")

    result_part2 = solution_part2(input)
    print(f"Solution to part 2: {result_part2}")
