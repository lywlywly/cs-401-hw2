import argparse
import os
import pickle
from itertools import combinations

data_dir = os.environ.get("DATA_DIR", "/data")


def prepare_rule():
    with open(os.path.join(data_dir, "ml/rule.pickle"), "rb") as file:
        rules_dict = pickle.load(file)

    return rules_dict


def recommend(rules_dict: dict[tuple[str], set[str]], input_tracks: list[str]):
    result = set()
    input_set = set(input_tracks)
    for t in full_combination(input_set):
        if s := rules_dict.get(t):
            result.update(s)

    return result - input_set


def full_combination(my_list):
    combinations_list = []
    for r in range(1, len(my_list) + 2):
        combinations_list.extend(list(combinations(my_list, r)))

    return combinations_list


def run(tracks):
    rules_dict = prepare_rule()
    print("Loaded rules...")
    return recommend(rules_dict, tracks)


def main():
    parser = argparse.ArgumentParser(description="Playlist recommendation.")
    parser.add_argument("-i", "--input", required=True, nargs="+", help="Input tracks.")
    args = parser.parse_args()
    tracks = args.input
    run(tracks)


main() if __name__ == "__main__" else None
