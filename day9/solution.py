from typing import Tuple, List
from copy import deepcopy
from tqdm import tqdm


def parse_input() -> List[List[str]]:
    input = []
    with open("input.txt") as file:
        for line in file:
            row = line.rstrip()
            processed_row = [int(c) for c in row]
            input = processed_row
        return input


def create_tuples(input: List[str]) -> List[Tuple[int, Tuple[int, int]]]:
    if len(input) % 2 != 0:
        input.append(0)

    it = iter(input)
    new_input = list(zip(it, it))
    return new_input


def construct_disk_map(input: List[str]):
    disk_map = []
    idx = 0
    for file, free_space in input:
        disk_map += [idx] * file
        disk_map += ["."] * free_space
        idx += 1

    return disk_map


def construct_disk_map_2(tuples: List[Tuple[int, Tuple[int, int]]]):
    disk_map = []
    idx = 0
    for file, description in tuples:
        file_size, free_space = description
        disk_map += [file] * file_size
        disk_map += ["."] * free_space
        idx += 1

    return disk_map


def part1(disk_map: List[str]):
    result = []
    files_in_reverse_indices = []
    for idx, file in enumerate(disk_map):
        if file != ".":
            files_in_reverse_indices.append(idx)

    file_count = len(files_in_reverse_indices)
    reverse_idx = len(files_in_reverse_indices) - 1

    for entry in disk_map:
        if len(result) == file_count:
            break
        if entry != ".":
            result.append(entry)
        else:
            result.append(disk_map[files_in_reverse_indices[reverse_idx]])
            reverse_idx -= 1

    checksum = 0
    for idx, val in enumerate(result):
        checksum += val * idx

    return checksum


def part2(tuples: List[Tuple[int, Tuple[int, int]]]):
    new_map = []
    for idx, entry in enumerate(tuples):
        new_map.append((idx, entry))

    new_map_copy = deepcopy(new_map)
    curr_disk_map = construct_disk_map_2(new_map_copy)

    unique_vals = set()
    for val in curr_disk_map:
        if val != ".":
            unique_vals.add(val)

    processed_files = set()
    processed_files.add(new_map_copy[0][0])

    tracker = {}
    for item in new_map_copy:
        tracker[item[0]] = (item[0], item[1])

    for idx, rev in tqdm(enumerate(reversed(new_map))):
        rev = tracker[rev[0]]
        new_ind = 0
        for ind, val in enumerate(new_map_copy):
            if val[0] == rev[0]:
                new_ind = ind

        if rev[0] in processed_files:
            idx += 1
            continue

        for int_idx, fwd in enumerate(new_map_copy[:new_ind]):
            if fwd[1][1] >= rev[1][0]:
                old_idx = new_map_copy.index(rev)
                for i, j in zip(
                    range(
                        curr_disk_map.index(fwd[0]) + fwd[1][0],
                        curr_disk_map.index(fwd[0]) + fwd[1][0] + rev[1][0],
                    ),
                    range(
                        curr_disk_map.index(rev[0]),
                        curr_disk_map.index(rev[0]) + rev[1][0],
                    ),
                ):
                    if curr_disk_map[i] == ".":
                        curr_disk_map[i] = rev[0]

                    if curr_disk_map[j] == rev[0]:
                        curr_disk_map[j] = "."

                new_map_copy[old_idx - 1] = (
                    new_map_copy[old_idx - 1][0],
                    (
                        new_map_copy[old_idx - 1][1][0],
                        new_map_copy[old_idx - 1][1][1]
                        + new_map_copy[old_idx][1][0]
                        + new_map_copy[old_idx][1][1],
                    ),
                )
                tracker[new_map_copy[old_idx - 1][0]] = new_map_copy[old_idx - 1]
                new_map_copy.pop(old_idx)
                new_map_copy[int_idx] = (fwd[0], (fwd[1][0], 0))
                tracker[new_map_copy[int_idx][0]] = (
                    new_map_copy[int_idx][0],
                    (fwd[1][0], 0),
                )

                new_map_copy.insert(
                    int_idx + 1, (rev[0], (rev[1][0], fwd[1][1] - rev[1][0]))
                )
                tracker[rev[0]] = (rev[0], (rev[1][0], fwd[1][1] - rev[1][0]))
                break
        processed_files.add(rev[0])

    checksum = 0
    for idx, val in enumerate(curr_disk_map):
        if val != ".":
            checksum += val * idx

    return checksum


if __name__ == "__main__":
    input_list = parse_input()
    parsed_input = create_tuples(input_list)
    disk_map = construct_disk_map(parsed_input)
    result_part1 = part1(disk_map=disk_map)
    print(f"Solution part 1: {result_part1}")
    result_part2 = part2(parsed_input)
    print(f"Solution part 2: {result_part2}")
