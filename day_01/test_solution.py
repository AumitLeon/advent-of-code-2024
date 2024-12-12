from solution import parse_input, compute_distances, similiarity_score


def test_parse_input():
    list1, list2 = parse_input()
    assert len(list1) == len(list2) == 1000


def test_compute_distances():
    list1, list2 = parse_input()
    assert compute_distances(list1, list2) == 2166959


def test_similarity_score():
    list1, list2 = parse_input()
    assert similiarity_score(list1, list2) == 23741109
