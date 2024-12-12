from typing import List, Tuple
import itertools


def parse_input() -> Tuple[List[List[str]], Tuple[int, int]]:
    input = []
    with open("input.txt") as file:
        for line in file:
            row = line.rstrip().split(":")
            processed_row = [c.rstrip() for c in row[1].split(" ")[1:]]
            input.append((row[0], processed_row))

        return input


def get_operator_combos(length: int):
    return list(itertools.product(["+", "*"], repeat=length))


def get_operator_combos_2(length: int):
    return list(itertools.product(["+", "*", "||"], repeat=length))


def part_1(input: List[str]) -> int:
    results = []
    for operation in input:
        result, operands = operation
        for operator_order in get_operator_combos_2(len(operands) - 1):
            result_for_combo = 0
            for idx, _ in enumerate(operands):
                if idx != len(operands) - 1:
                    operator = operator_order[idx]
                    if idx == 0:
                        if operator == "+":
                            result_for_combo = int(operands[idx]) + int(
                                operands[idx + 1]
                            )

                        elif operator == "*":
                            result_for_combo = int(operands[idx]) * int(
                                operands[idx + 1]
                            )
                    else:
                        if operator == "+":
                            result_for_combo += int(operands[idx + 1])
                        elif operator == "*":
                            result_for_combo *= int(operands[idx + 1])

            if result_for_combo == int(result):
                results.append(int(result))
                break
    return sum(results)


def part_2(input: List[str]) -> int:
    results = []
    for operation in input:
        result, operands = operation
        for operator_order in get_operator_combos_2(len(operands) - 1):
            result_for_combo = 0
            for idx, operand in enumerate(operands):
                if idx != len(operands) - 1:
                    operator = operator_order[idx]
                    if idx == 0:
                        if operator == "+":
                            result_for_combo = int(operands[idx]) + int(
                                operands[idx + 1]
                            )

                        elif operator == "*":
                            result_for_combo = int(operands[idx]) * int(
                                operands[idx + 1]
                            )
                        elif operator == "||":
                            result_for_combo = int(operands[idx] + operands[idx + 1])

                    else:
                        if operator == "+":
                            result_for_combo += int(operands[idx + 1])
                        elif operator == "*":
                            result_for_combo *= int(operands[idx + 1])
                        elif operator == "||":
                            result_for_combo = int(
                                str(result_for_combo) + operands[idx + 1]
                            )

            if result_for_combo == int(result):
                results.append(int(result))
                break
    return sum(results)


if __name__ == "__main__":
    input = parse_input()
    result_part1 = part_1(input=input)
    print(f"Solution part 1: {result_part1}")

    result_part2 = part_2(input=input)
    print(f"Solution part 2: {result_part2}")
