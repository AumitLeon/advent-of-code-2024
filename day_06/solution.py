from typing import List, Tuple, Dict
from copy import deepcopy
from tqdm import tqdm


def parse_input() -> Tuple[List[List[str]], Tuple[int, int]]:
    lines = []
    start_x_pos = None
    start_y_pos = 0
    found_row = False
    with open("input.txt") as file:
        for line in file:
            row = line.rstrip()
            processed_row = [c for c in row]
            if "^" in processed_row:
                start_x_pos = processed_row.index("^")
                found_row = True
            lines.append(processed_row)
            if not found_row:
                start_y_pos += 1

    return lines, (start_x_pos, start_y_pos)


def get_next_position(x: int, y: int, orientation: str) -> Tuple[int, int]:
    if orientation == "NORTH":
        return (x, y - 1)
    elif orientation == "SOUTH":
        return (x, y + 1)
    elif orientation == "EAST":
        return (x + 1, y)
    elif orientation == "WEST":
        return (x - 1, y)


def is_obstacle(x: int, y: int, matrix: List[List[str]]) -> bool:
    return True if matrix[y][x] in ("#", "O") else False


def is_out_of_bounds(x: int, y: int, matrix: List[List[str]]) -> bool:
    matrix_x_dimension = len(matrix[0])
    matrix_y_dimension = len(matrix)
    if 0 > x or x > matrix_x_dimension - 1 or 0 > y or y > matrix_y_dimension - 1:
        return True
    else:
        return False


def is_visited(x, y, matrix):
    return True if matrix[y][x] == "X" else False


def visit(x: int, y: int, matrix: List[List[str]]) -> List[List[str]]:
    matrix[y][x] = "X"
    return matrix


def get_new_orientation(current_orientation: str):
    # Always turn 90 degrees to the right
    if current_orientation == "NORTH":
        return "EAST"
    elif current_orientation == "EAST":
        return "SOUTH"
    elif current_orientation == "SOUTH":
        return "WEST"
    elif current_orientation == "WEST":
        return "NORTH"


def count_visited(
    matrix: List[List[str]], coords: Tuple[int, int], orientation: str
) -> int:
    # Mark the starting position
    matrix = visit(coords[0], coords[1], matrix)
    visited = 1

    # Locate the next position.
    first_position = get_next_position(
        x=coords[0], y=coords[1], orientation=orientation
    )
    x = first_position[0]
    y = first_position[1]

    while not is_out_of_bounds(x, y, matrix):
        possible_x, possible_y = get_next_position(x, y, orientation)
        if is_out_of_bounds(possible_x, possible_y, matrix):
            if not is_visited(x, y, matrix):
                matrix = visit(x, y, matrix)
                visited += 1
            break
        if is_obstacle(possible_x, possible_y, matrix):
            # Rotate orientation
            if not is_visited(x, y, matrix):
                matrix = visit(x, y, matrix)
                visited += 1

            # Define temp vars to be used for the rotation
            temp_x, temp_y = possible_x, possible_y
            while is_obstacle(temp_x, temp_y, matrix):
                orientation = get_new_orientation(current_orientation=orientation)
                x, y = get_next_position(x, y, orientation)
                temp_x, temp_y = x, y
        else:
            if not is_visited(x, y, matrix):
                matrix = visit(x, y, matrix)
                visited += 1
            x, y = get_next_position(x, y, orientation)
    return visited


def get_all_current_obstacles(matrix: List[List[str]]) -> List[Tuple[int]]:
    # Get all positions of the obstacles
    current_obstacle_positions = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == "#":
                current_obstacle_positions.append((i, j))
    return current_obstacle_positions


def construct_obstacle_visited_cache(matrix: List[List[str]]):
    current_obstacle_positions = get_all_current_obstacles(matrix)
    obstacle_cache = {}
    for pos in current_obstacle_positions:
        obstacle_cache[pos] = {"NORTH": 0, "SOUTH": 0, "EAST": 0, "WEST": 0}
    return obstacle_cache


def is_loop(
    matrix: List[List[str]],
    start_coords: Tuple[int, int],
    visited_obstacle_cache: Dict[Tuple[int, int], int],
    orientation: str,
):
    # Mark the starting position
    matrix = visit(start_coords[0], start_coords[1], matrix)
    first_position = get_next_position(
        x=start_coords[0], y=start_coords[1], orientation=orientation
    )

    x = first_position[0]
    y = first_position[1]
    while not is_out_of_bounds(x, y, matrix):
        possible_x, possible_y = get_next_position(x, y, orientation)
        if is_out_of_bounds(possible_x, possible_y, matrix):
            if not is_visited(x, y, matrix):
                matrix = visit(x, y, matrix)
            return False
        if is_obstacle(possible_x, possible_y, matrix):
            # Rotate orientation
            if not is_visited(x, y, matrix):
                matrix = visit(x, y, matrix)

            temp_x, temp_y = possible_x, possible_y
            orig_x, orig_y = x, y
            while is_obstacle(temp_x, temp_y, matrix):
                visited_obstacle_cache[(temp_y, temp_x)][orientation] += 1
                for obs in visited_obstacle_cache:
                    if visited_obstacle_cache[obs][orientation] > 1:
                        return True
                orientation = get_new_orientation(current_orientation=orientation)
                x, y = get_next_position(orig_x, orig_y, orientation)
                temp_x, temp_y = x, y
        else:
            if not is_visited(x, y, matrix):
                matrix = visit(x, y, matrix)
            x, y = get_next_position(x, y, orientation)

    return True


def is_valid_obstacle_position(x: int, y: int, matrix: List[List[str]]):
    if matrix[y][x] in ("#", "^"):
        # Can't place an obstacle at the starting position or at the position of an existing obstacle.
        return False
    else:
        return True


def find_possible_loops(matrix: List[List[str]], coords: Tuple[int, int]):
    visited_obstacle_cache = construct_obstacle_visited_cache(matrix)
    new_obstacle_positions = []
    for row in tqdm(range(len(matrix))):
        for column in range(len(matrix[row])):
            current_matrix = deepcopy(matrix)
            current_obstacle_visited_cache = deepcopy(visited_obstacle_cache)
            if is_valid_obstacle_position(column, row, current_matrix):
                # Place the new obstacle
                current_matrix[row][column] = "O"

                # Add it to our cache dictionary
                current_obstacle_visited_cache[(row, column)] = {
                    "NORTH": 0,
                    "SOUTH": 0,
                    "EAST": 0,
                    "WEST": 0,
                }

                # Traverse, and see if we've created a loop.
                if is_loop(
                    matrix=current_matrix,
                    start_coords=coords,
                    visited_obstacle_cache=current_obstacle_visited_cache,
                    orientation="NORTH",
                ):
                    new_obstacle_positions.append((row, column))

    return new_obstacle_positions


def print_matrix(matrix: List[List[str]]):
    for row in matrix:
        print("".join(row))


if __name__ == "__main__":
    matrix, start_coords = parse_input()
    # We modify the matrix in part 1 in place, so make a deep copy for part 2.
    matrix_for_part2 = deepcopy(matrix)

    result_part1 = count_visited(
        matrix=matrix, coords=start_coords, orientation="NORTH"
    )
    print(f"Solution for part 1: {result_part1}")

    loops = find_possible_loops(matrix_for_part2, start_coords)
    print(f"Solution for part 2: {len(loops)}")
