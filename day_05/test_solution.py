from solution import (
    parse_input,
    process_updates,
    sum_medians,
    reprocess_bad_updates,
    construct_ruleset,
)


def test_parse_input():
    rules, updates = parse_input()
    assert len(rules) == 1176 and len(updates) == 223


def test_process_updates():
    rules, updates = parse_input()
    good_updates, bad_updates = process_updates(rules=rules, updates=updates)
    assert len(good_updates) == 106
    assert len(bad_updates) == 117
    assert sum_medians(good_updates=good_updates) == 6505


def test_reprocess_bad_updates():
    raw_rules, updates = parse_input()
    rule_set = construct_ruleset(raw_rules)
    good_updates, bad_updates = process_updates(rules=raw_rules, updates=updates)
    updated_bad_updates = reprocess_bad_updates(bad_updates=bad_updates, rules=rule_set)
    assert sum_medians(good_updates=updated_bad_updates) == 6897


# def test_solution_part2():
#     matrix = parse_input()
#     assert solution_part2(matrix) == 1974
