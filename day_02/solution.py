from typing import List


def parse_input() -> List[List[int]]:
    reports = []
    with open("input.txt") as file:
        for line in file:
            # Split by space in input, strip trailing spaces.
            input_report = line.rstrip().split(" ")
            reports.append([int(level) for level in input_report])
    return reports


def is_report_safe(levels: List[int], index_ignore: int = None):
    if index_ignore == 0:
        prev_level = levels[1]
        first_index = 1
    else:
        prev_level = levels[0]
        first_index = 0
    increasing = None
    for idx in range(0, len(levels)):
        # If we're on the last element of the list and this is the index to ignore, mark as safe.
        if idx == index_ignore and index_ignore == len(levels) - 1:
            return True
        # If we're on the index to ignore, skip.
        if idx == index_ignore:
            continue
        curr_level = levels[idx]
        # Always skip the first index, no comparison can be made here.
        if idx == first_index:
            continue
        # If we're not ignoring the previous index,
        if index_ignore and index_ignore != idx - 1:
            prev_level = levels[idx - 1]
        # If we're going to ignore the second element, and we're on the third element, determine if we should be monotonoically increasing or decreasing.
        if index_ignore == 1 and idx == 2:
            if curr_level > prev_level:
                increasing = True
            elif curr_level < prev_level:
                increasing = False
            else:
                break
        # In the default case, if we're on the second element, determine if we should be monotonically increasing or decreasing.
        elif idx == first_index + 1:
            if curr_level > prev_level:
                increasing = True
            elif curr_level < prev_level:
                increasing = False
            else:
                break

        if increasing and prev_level > curr_level:
            break
        elif not increasing and curr_level > prev_level:
            break
        elif prev_level == curr_level:
            break
        elif 3 >= abs(curr_level - prev_level) >= 1:
            prev_level = levels[idx]
            if idx == len(levels) - 1:
                return True
        else:
            break
    return False


def get_number_of_safe_reports_part_1(reports: List[List[int]]) -> int:
    num_safe_reports = 0
    not_safe_reports = []
    for levels in reports:
        is_safe = is_report_safe(levels)
        if is_safe:
            num_safe_reports += 1
        else:
            not_safe_reports.append(levels)
    return num_safe_reports


def get_number_of_safe_reports_part_2(reports: List[List[int]]) -> int:
    num_safe_reports = 0
    for levels in reports:
        # Check if the unmodified report is safe.
        is_safe = is_report_safe(levels)
        if is_safe:
            num_safe_reports += 1
            continue
        else:
            # Loop over and see if removing any individual element from the report produces a safe report
            for idx, level in enumerate(levels):
                if is_report_safe(levels, idx):
                    num_safe_reports += 1
                    break
    return num_safe_reports


if __name__ == "__main__":
    reports = parse_input()
    num_safe_reports = get_number_of_safe_reports_part_1(reports)
    print(num_safe_reports)

    num_safe_reports_2 = get_number_of_safe_reports_part_2(reports)
    print(num_safe_reports_2)
