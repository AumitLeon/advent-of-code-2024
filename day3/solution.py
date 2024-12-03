from typing import List


def parse_input() -> List[List[int]]:
    lines = []
    with open("input.txt") as file:
        for line in file:
            input = line.rstrip()
            lines.append(input)
    return lines


def _construct_operands_and_aggregate_result(split_delimited_instructions: List[str]):
    aggregator = 0
    operands = [
        val
        for val in split_delimited_instructions
        if 7 >= len(val) >= 3 and val[0].isdigit() and val[-1].isdigit()
    ]

    for pair in operands:
        operand1, operand2 = pair.split(",")
        aggregator += int(operand1) * int(operand2)

    return aggregator


def multiply(instructions: List[str]) -> int:
    result = 0
    for instruction in instructions:
        # Delmit the mul instructions to identify them.
        delimited_instruction = instruction.replace("mul(", "DELIMITER").replace(
            ")", "DELIMITER"
        )
        split_delimited_instructions = delimited_instruction.split("DELIMITER")

        result += _construct_operands_and_aggregate_result(
            split_delimited_instructions=split_delimited_instructions
        )

    return result


def multiply_part2(instructions: List[str]):
    do = True
    result = 0
    for instruction in instructions:
        delimited_instruction = instruction.replace(
            "don't()", "DELIMITERdon't()DELIMITER"
        ).replace("do()", "DELIMITERdo()DELIMITER")
        split_delimited_instruction = delimited_instruction.split("DELIMITER")
        for parsed_instruction in split_delimited_instruction:
            if parsed_instruction == "do()":
                do = True
                continue
            elif parsed_instruction == "don't()":
                do = False
                continue
            if do:
                delimited_parsed_instruction = parsed_instruction.replace(
                    "mul(", "MULDELIMITER"
                ).replace(")", "MULDELIMITER")
                split_delimited_parsed_instruction = delimited_parsed_instruction.split(
                    "MULDELIMITER"
                )
                result += _construct_operands_and_aggregate_result(
                    split_delimited_instructions=split_delimited_parsed_instruction
                )
    return result


if __name__ == "__main__":
    input = parse_input()
    part1_result = multiply(input)
    print(f"Part 1 result: {part1_result}")
    part2_result = multiply_part2(input)
    print(f"Part 2 result: {part2_result}")
