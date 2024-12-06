from typing import List, Tuple, Dict


def parse_input() -> Tuple[List[str], List[str]]:
    updates = []
    rules = []
    with open("input.txt") as file:
        for line in file:
            row = line.rstrip()
            if "|" in row:
                rules.append(row)
            elif "," in row:
                updates.append(row)
    return rules, updates


def process_updates(rules: List[str], updates: List[str]):
    good_updates = []
    bad_updates = []
    for string_update in updates:
        update = string_update.split(",")
        good = True
        # Make the list update a set, to get uniques
        unique_updates = set(update)
        possible_rules = set()
        actual_rules = set()
        for idx, page in enumerate(list(unique_updates)):
            for temp_page in list(unique_updates)[idx + 1 :]:
                possible_rules.add(f"{page}|{temp_page}")
                possible_rules.add(f"{temp_page}|{page}")

        # Now we look up the rules that exist
        for rule in possible_rules:
            if rule in set(rules):
                actual_rules.add(rule)

        for rule in actual_rules:
            # Parse and evaluate the rule
            page1, page2 = rule.split("|")
            if update.index(page1) > update.index(page2):
                good = False
                break
        if not good:
            bad_updates.append(update)
        else:
            good_updates.append(update)

    return good_updates, bad_updates


def construct_ruleset(actual_rules: List[str]) -> Dict[str, List[str]]:
    rule_set = {}
    all_pages = set()
    for rule in actual_rules:
        page1, page2 = rule.split("|")
        if page1 in rule_set:
            rule_set[page1].append(page2)
        else:
            rule_set[page1] = [page2]
        all_pages.add(page1)
        all_pages.add(page2)

    for page in all_pages:
        if page not in rule_set:
            # If a gien page doesn't have a rulset, just give it an empty list.
            rule_set[page] = []

    return rule_set


def sum_medians(good_updates: List[str]) -> int:
    result = 0
    for update in good_updates:
        result += int(update[int(len(update) / 2)])

    return result


def reprocess_bad_updates(
    bad_updates: List[str], rules: Dict[str, List[str]]
) -> List[str]:
    good_updates = []
    for update in bad_updates:
        corrected_update = []
        for page in update:
            new_list = []
            # All the pages that should be after the current processing page
            later_pages = rules[page]
            # Get the index of the the earliest page in the corrected string of the pages that are greater than the current page.
            page_idx = min(
                (
                    corrected_update.index(p)
                    for p in later_pages
                    if p in corrected_update
                ),
                default=-1,
            )
            if page_idx != -1:
                val_to_replace = corrected_update[page_idx]
                if page_idx == 0:
                    # Replace first
                    new_list = [page] + corrected_update
                elif page_idx == len(corrected_update) - 1:
                    # Replace last
                    new_list = corrected_update[:page_idx] + [page, val_to_replace]
                else:
                    # Replace middle
                    new_list = (
                        corrected_update[:page_idx]
                        + [page, val_to_replace]
                        + corrected_update[-len(corrected_update) + page_idx + 1 :]
                    )
            else:
                # Just append if there's no rule that implies where we should insert the current page.
                new_list = corrected_update + [page]
            corrected_update = new_list

        good_updates.append(corrected_update)

    return good_updates


if __name__ == "__main__":
    raw_rules, updates = parse_input()
    good_updates, bad_updates = process_updates(raw_rules, updates)
    result_part1 = sum_medians(good_updates)
    print(f"Solution for part 1: {result_part1}")

    rule_set = construct_ruleset(raw_rules)
    updated_bad = reprocess_bad_updates(bad_updates, rule_set)
    result_part2 = sum_medians(updated_bad)
    print(f"Solution for part 2: {result_part2}")
