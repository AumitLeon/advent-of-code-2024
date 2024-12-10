from typing import List, Tuple, Dict


def parse_input() -> Tuple[List[List[int]], List[Tuple[int, int]]]:
    matrix = []
    start_row_pos = 0
    trail_starts = []
    with open("input.txt") as file:
        for line in file:
            row = line.rstrip()
            processed_row = [int(c) for c in row]

            processed_row = []
            for idx, c in enumerate(row):
                if c == "0":
                    trail_starts.append((start_row_pos, idx))
                processed_row.append(int(c))
            matrix.append(processed_row)
            start_row_pos += 1

    return matrix, trail_starts


def is_valid_pos(row: int, col: int, matrix: List[List[str]], cur_height: int) -> bool:
    matrix_col_dimension = len(matrix[0])
    matrix_row_dimension = len(matrix)
    if (
        0 > col
        or col > matrix_col_dimension - 1
        or 0 > row
        or row > matrix_row_dimension - 1
        or matrix[row][col] != cur_height + 1
    ):
        return False
    else:
        return True


def get_possible_positions(row_idx: int, column_idx: int) -> List[Tuple[int, int]]:
    return [
        (row_idx + 1, column_idx),  # Below
        (row_idx - 1, column_idx),  # Above
        (row_idx, column_idx + 1),  # Right
        (row_idx, column_idx - 1),  # Left
    ]


def traverse_trails(
    matrix: List[List[int]],
    start_coords: Tuple[int, int],
    curr_height: int,
    visited_peaks: Dict[Tuple[int, int], bool],
):
    row, col = start_coords
    possible_positions = get_possible_positions(row, col)
    for pos in possible_positions:
        next_row, next_col = pos
        if is_valid_pos(next_row, next_col, matrix, curr_height):
            if curr_height == 8 and matrix[next_row][next_col] == 9:
                if pos not in visited_peaks:
                    visited_peaks[pos] = 1
            else:
                traverse_trails(
                    matrix, (next_row, next_col), curr_height + 1, visited_peaks
                )
    return visited_peaks


def count_trails(matrix, trail_starts):
    total_trails = 0
    for start in trail_starts:
        row, col = start
        curr_height = 0
        visited_peaks = {}
        visited_peaks = traverse_trails(matrix, (row, col), curr_height, visited_peaks)
        total_trails += len(visited_peaks)
    return total_trails


def traverse_trails_2(
    matrix: List[List[int]], start_coords: Tuple[int, int], curr_height: int
) -> int:
    row, col = start_coords

    if curr_height == 9 and matrix[row][col] == 9:
        return 1

    possible_positions = get_possible_positions(row, col)
    result = 0
    for pos in possible_positions:
        next_row, next_col = pos
        if is_valid_pos(next_row, next_col, matrix, curr_height):
            result += traverse_trails_2(matrix, (next_row, next_col), curr_height + 1)

    return result


def count_ratings(matrix: List[List[int]], trail_starts: Tuple[int, int]) -> int:
    total_ratings = 0
    for start in trail_starts:
        row, col = start
        curr_height = 0
        total_ratings += traverse_trails_2(matrix, (row, col), curr_height)
    return total_ratings


def print_trail_starts(matrix: List[List[int]], trail_starts: Tuple[int, int]):
    count = 1
    for coord in trail_starts:
        row, col = coord
        print(f"{count}: {coord} -- {matrix[row][col]}")
        count += 1


if __name__ == "__main__":
    matrix, trail_starts = parse_input()

    result_part1 = count_trails(matrix, trail_starts)
    print(f"Solution for part 1: {result_part1}")

    result_part2 = count_ratings(matrix, trail_starts)
    print(f"Solution for part 2: {result_part2}")
