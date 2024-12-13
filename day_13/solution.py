from typing import List, Tuple
import numpy as np


def parse_input(part: int) -> Tuple[List[List[int]], List[Tuple[int, int]]]:
    values = []
    temp = []
    with open("input.txt") as file:
        for line in file:
            if line == "\n":
                values.append(temp)
                temp = []
                continue
            row = line.rstrip()
            split_row = row.split(" ")
            if split_row[0] == "Prize:":
                if part == 1:
                    x = int(split_row[1].split(",")[0].split("=")[1])
                    y = int(split_row[2].split("=")[1])
                elif part == 2:
                    x = int(
                        10000000000000 + int(split_row[1].split(",")[0].split("=")[1])
                    )
                    y = int(10000000000000 + int((split_row[2].split("=")[1])))
            elif split_row[0] == "Button":
                x = int(split_row[2].split(",")[0].split("+")[1])
                y = int(split_row[3].split("+")[1])
            temp.append((x, y))
    values.append(temp)
    return values


def parse_input_2() -> List[Tuple[int, int, int]]:
    values = []
    temp = []
    with open("input.txt") as file:
        for line in file:
            if line == "\n":
                values.append(temp)
                temp = []
                continue
            row = line.rstrip()
            # print(row)
            split_row = row.split(" ")
            if split_row[0] == "Prize:":
                x = int(10000000000000 + int(split_row[1].split(",")[0].split("=")[1]))
                y = int(10000000000000 + int((split_row[2].split("=")[1])))
            elif split_row[0] == "Button":
                x = int(split_row[2].split(",")[0].split("+")[1])
                y = int(split_row[3].split("+")[1])
            # print(f"{x} -- {y}")
            temp.append((x, y))
    values.append(temp)
    return values


def solve_system_of_equations(equations: List[Tuple[int, int, int]]):
    tokens = 0

    for eq in equations:
        x1 = eq[0][0]
        x2 = eq[1][0]
        y1 = eq[0][1]
        y2 = eq[1][1]

        prize_x = eq[2][0]
        prize_y = eq[2][1]

        # Define the coefficients matrix and the constants vector
        A = np.array([[x1, x2], [y1, y2]])
        b = np.array([prize_x, prize_y])
        # Solve the system of equations
        x = np.linalg.solve(A, b)

        rounded_solution = np.round(x, decimals=3, out=None)
        mask = (rounded_solution % 1) == 0
        if np.all(mask):
            # This is a solution -- increment the tokens
            tokens += rounded_solution[0] * 3 + rounded_solution[1]

    return tokens


if __name__ == "__main__":
    part_1_values = parse_input(part=1)
    result_part1 = solve_system_of_equations(part_1_values)
    print(f"Solution part 1: {result_part1}")

    part_2_values = parse_input(part=2)
    result_part_2 = solve_system_of_equations(part_2_values)
    print(f"Solution part 2: {result_part_2}")
