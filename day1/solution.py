from collections import Counter
from typing import List, Tuple


def parse_input() -> Tuple[List[int], List[int]]:
    list1 = []
    list2 = []
    with open("input.txt") as file:
        for line in file:
            # Split by double space in input
            input_elements = line.rstrip().split("  ")
            list1.append(int(input_elements[0]))
            list2.append(int(input_elements[1]))
    return list1, list2


def compute_distances(list1: List[int], list2: List[int]) -> int:
    total = 0
    # Sort both lists
    for x, y in zip(sorted(list1), sorted(list2)):
        total += abs(x - y)
    return total


def similiarity_score(list1: List[int], list2: List[int]) -> int:
    # Get counts of each number in list2
    score = 0
    list2_counter = Counter(list2)
    for i in list1:
        score += i * list2_counter[i]
    return score


if __name__ == "__main__":
    print("Beginning solution")
    # Parse input
    list1, list2 = parse_input()

    distance = compute_distances(list1, list2)
    print(f"Total distance is: {distance}")

    score = similiarity_score(list1, list2)
    print(f"Total similarity score is: {score}")
