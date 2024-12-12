from typing import List
import re


def parse_input() -> List[List[int]]:
    lines = []
    with open("input.txt") as file:
        for line in file:
            input = line.rstrip()
            lines.append(input)
    return lines


def multiply(instructions: List[str]) -> int:
    result = 0
    for instruction in instructions:
        # Below regex matches "mul" followed by a number made of 1-3 digits, followed by "," followed by another number made of 1-3 digits.
        matches = re.findall(r"mul\([0-9]{1,3},[0-9]{1,3}\)", instruction)
        for match in matches:
            # Grab the operands from the match
            operand1, operand2 = re.findall("[0-9]{1,3}", match)
            result += int(operand1) * int(operand2)
    return result


def multiply_part2(instructions: List[str]) -> int:
    result = 0
    do = True
    for instruction in instructions:
        # The regex pattern below matches "do()"
        # OR "mul" followed by a number made of 1-3 digits, followed by "," followed by another number made of 1-3 digits,
        # OR "don't()"
        matches = re.findall(
            r"do\(\)|mul\([0-9]{1,3},[0-9]{1,3}\)|don't\(\)", instruction
        )
        for match in matches:
            if match == "do()":
                do = True
                continue
            elif match == "don't()":
                do = False
                continue
            if do:
                operand1, operand2 = re.findall("[0-9]{1,3}", match)
                result += int(operand1) * int(operand2)
    return result


if __name__ == "__main__":
    input = parse_input()
    part1_result = multiply(input)
    print(f"Part 1 result: {part1_result}")
    part2_result = multiply_part2(input)
    print(f"Part 2 result: {part2_result}")
