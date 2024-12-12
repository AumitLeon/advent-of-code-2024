from typing import List
from copy import deepcopy
from tqdm import tqdm
from functools import cache


def parse_input() -> List[str]:
    stones = []
    with open("input.txt") as file:
        for line in file:
            row = line.rstrip().split(" ")
            stones = row

    return stones


@cache
def split_even(stone: str) -> List[str]:
    new_stones = []

    new_stones.append(stone[: int(len(stone) / 2)])
    if stone[int(len(stone) / 2) :][0] == "0":
        split2 = stone[int(len(stone) / 2) :]
        new_offset = 0
        for idx, c in enumerate(split2):
            if c != "0":
                new_offset = idx
                break
            elif idx == len(split2) - 1:
                new_offset = idx
        new_stones.append(split2[new_offset:])
    else:
        new_stones.append(stone[int(len(stone) / 2) :])
    return new_stones


@cache
def mult(x: str, y: int):
    return str(int(x) * y)


@cache
def check_length(val):
    return len(val) % 2 == 0


def mark_stone_visited(seen_stones, stone, cnt=None):
    if stone not in seen_stones:
        seen_stones[stone] = 1 if not cnt else cnt
    else:
        seen_stones[stone] += 1 if not cnt else cnt


def part_1(stones):
    temp_stones = deepcopy(stones)
    for _ in tqdm(range(0, 25)):
        new_temp_stones = []
        for stone in temp_stones:
            if stone == "0":
                new_temp_stones.append("1")

            elif len(stone) % 2 == 0:
                new_temp_stones.extend(split_even(stone))
            else:
                new_temp_stones.append(mult(stone, 2024))
        temp_stones = new_temp_stones

    return len(temp_stones)


def part_2(stones):
    seen_stones = {}
    for stone in stones:
        if stone not in seen_stones:
            seen_stones[stone] = 1
        else:
            seen_stones[stone] += 1
    counter = len(stones)
    for _ in tqdm(range(75)):
        curr_map = {}
        for stone, cnt in seen_stones.items():
            if stone == "0":
                mark_stone_visited(curr_map, "1", cnt)
            elif check_length(stone):
                split1, split2 = split_even(stone)
                counter += cnt
                # Add both splits to the current map
                mark_stone_visited(curr_map, split1, cnt)
                mark_stone_visited(curr_map, split2, cnt)
            else:
                mark_stone_visited(curr_map, mult(stone, 2024), cnt)

        seen_stones = curr_map

    return counter


if __name__ == "__main__":
    stones = parse_input()
    result_part1 = part_1(stones)
    print(f"Solution part 1: {result_part1}")

    result_part2 = part_2(stones)
    print(f"Solution part 2: {result_part2}")
