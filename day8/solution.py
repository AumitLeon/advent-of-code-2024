from typing import List, Tuple, Dict


def parse_input() -> Tuple[List[List[str]], Dict[str, Tuple[int, int]]]:
    matrix = []
    nodes = {}
    row_idx = 0
    with open("input.txt") as file:
        for line in file:
            row = line.rstrip()
            processed_row = [c.rstrip() for c in row]
            for column_idx, item in enumerate(processed_row):
                if item.isalnum():
                    if item not in nodes:
                        nodes[item] = [(row_idx, column_idx)]
                    else:
                        nodes[item].append((row_idx, column_idx))

            matrix.append(processed_row)
            row_idx += 1

        return matrix, nodes


def print_matrix(matrix: List[List[str]]):
    for row in matrix:
        print("".join(row))


def get_antinodes(
    current_coord: Tuple[int, int], compare_coord: Tuple[int, int]
) -> List[Tuple[int, int]]:
    row1, col1 = current_coord
    row2, col2 = compare_coord

    abs_row = abs(row1 - row2)
    abs_col = abs(col1 - col2)

    if row1 < row2 and col1 > col2:
        return [(row1 - abs_row, col1 + abs_col), (row2 + abs_row, col2 - abs_col)]
    elif row1 < row2 and col1 < col2:
        return [(row1 - abs_row, col1 - abs_col), (row2 + abs_row, col2 + abs_col)]


def is_out_of_bounds(row: int, column: int, matrix: List[List[str]]) -> bool:
    matrix_column_dimension = len(matrix[0])
    matrix_row_dimension = len(matrix)
    if (
        0 > column
        or column > matrix_column_dimension - 1
        or 0 > row
        or row > matrix_row_dimension - 1
    ):
        return True
    else:
        return False


def part_1(matrix: List[List[str]], nodes: Dict[str, Tuple[int, int]]):
    anti_node_map = {}
    for node, list_of_coords in nodes.items():
        for idx in range(len(list_of_coords)):
            current_coord = list_of_coords[idx]
            if idx != len(list_of_coords):
                for compare_coord in list_of_coords[idx + 1 :]:
                    anti_nodes = get_antinodes(current_coord, compare_coord)
                    for anti_node in anti_nodes:
                        if not is_out_of_bounds(
                            matrix=matrix, row=anti_node[0], column=anti_node[1]
                        ):
                            if anti_node not in anti_node_map:
                                anti_node_map[anti_node] = [node]
                            else:
                                anti_node_map[anti_node].append(node)
    return len(anti_node_map)


def get_antinodes_2(
    current_coord: Tuple[int, int],
    compare_coord: Tuple[int, int],
    matrix: List[List[str]],
) -> List[Tuple[int, int]]:
    row1, col1 = current_coord
    row2, col2 = compare_coord

    abs_row = abs(row1 - row2)
    abs_col = abs(col1 - col2)
    antinodes = []
    temp_row1 = row1
    temp_row2 = row2
    temp_col1 = col1
    temp_col2 = col2
    antinodes.append(current_coord)
    antinodes.append(compare_coord)
    if row1 < row2 and col1 > col2:
        temp_row1 = temp_row1 - abs_row
        temp_col1 = temp_col1 + abs_col
        temp_row2 = temp_row2 + abs_row
        temp_col2 = temp_col2 - abs_col

        while not is_out_of_bounds(
            temp_row1, temp_col1, matrix
        ) or not is_out_of_bounds(temp_row2, temp_col2, matrix):
            if not is_out_of_bounds(temp_row1, temp_col1, matrix):
                antinodes.append((temp_row1, temp_col1))
                temp_row1 = temp_row1 - abs_row
                temp_col1 = temp_col1 + abs_col

            if not is_out_of_bounds(temp_row2, temp_col2, matrix):
                antinodes.append((temp_row2, temp_col2))
                temp_row2 = temp_row2 + abs_row
                temp_col2 = temp_col2 - abs_col

    elif row1 < row2 and col1 < col2:
        temp_row1 = temp_row1 - abs_row
        temp_col1 = temp_col1 - abs_col
        temp_row2 = temp_row2 + abs_row
        temp_col2 = temp_col2 + abs_col
        while not is_out_of_bounds(
            temp_row1, temp_col1, matrix
        ) or not is_out_of_bounds(temp_row2, temp_col2, matrix):
            if not is_out_of_bounds(temp_row1, temp_col1, matrix):
                antinodes.append((temp_row1, temp_col1))
                temp_row1 = temp_row1 - abs_row
                temp_col1 = temp_col1 - abs_col

            if not is_out_of_bounds(temp_row2, temp_col2, matrix):
                antinodes.append((temp_row2, temp_col2))
                temp_row2 = temp_row2 + abs_row
                temp_col2 = temp_col2 + abs_col
    return antinodes


def part_2(matrix: List[List[str]], nodes: Dict[str, List[Tuple[int, int]]]) -> int:
    anti_node_map = {}
    for node, list_of_coords in nodes.items():
        for idx in range(len(list_of_coords)):
            current_coord = list_of_coords[idx]
            if idx != len(list_of_coords):
                for compare_coord in list_of_coords[idx + 1 :]:
                    anti_nodes = get_antinodes_2(current_coord, compare_coord, matrix)
                    for anti_node in anti_nodes:
                        if not is_out_of_bounds(
                            matrix=matrix, row=anti_node[0], column=anti_node[1]
                        ):
                            if anti_node not in anti_node_map:
                                anti_node_map[anti_node] = [node]
                            else:
                                anti_node_map[anti_node].append(node)

    return len(anti_node_map)


if __name__ == "__main__":
    matrix, nodes = parse_input()

    result_part1 = part_1(matrix, nodes)
    print(f"Solution part1: {result_part1}")
    result_part2 = part_2(matrix, nodes)
    print(f"Solution part2: {result_part2}")
