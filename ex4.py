import math
from collections import Counter, defaultdict


# -----------------------------
# Read dataset from CSV file
# -----------------------------
def read_data(filename):
    with open(filename, 'r',encoding='utf-8-sig') as file:
        lines = file.read().strip().split('\n')

    headers = lines[0].split(',')
    data = []

    for line in lines[1:]:
        values = line.split(',')
        row = dict(zip(headers, values))
        data.append(row)

    return headers, data


# -----------------------------
# Manual Input
# -----------------------------
def manual_input():
    n = int(input("Enter number of records: "))
    headers = input("Enter attributes (comma separated): ").split(',')

    data = []
    for i in range(n):
        print(f"\nEnter record {i+1} values (comma separated):")
        values = input().split(',')
        row = dict(zip(headers, values))
        data.append(row)

    return headers, data


# -----------------------------
# Entropy Calculation
# -----------------------------
def entropy(data, target_attr):
    total = len(data)
    counts = Counter([row[target_attr] for row in data])

    print("\nClass Counts:", counts)

    ent = 0
    for cls, count in counts.items():
        p = count / total
        print(f"P({cls}) = {count}/{total} = {p}")
        ent -= p * math.log2(p)

    print("Entropy =", ent)
    return ent


# -----------------------------
# Gini Index
# -----------------------------
def gini_index(data, target_attr):
    total = len(data)
    counts = Counter([row[target_attr] for row in data])

    print("\nClass Counts:", counts)

    gini = 1
    for cls, count in counts.items():
        p = count / total
        print(f"P({cls}) = {count}/{total} = {p}")
        gini -= p ** 2

    print("Gini Index =", gini)
    return gini


# -----------------------------
# Split Dataset
# -----------------------------
def split_data(data, attr):
    splits = defaultdict(list)
    for row in data:
        splits[row[attr]].append(row)
    return splits


# -----------------------------
# Information Gain
# -----------------------------
def information_gain(data, attr, target_attr):
    print(f"\nCalculating Information Gain for attribute: {attr}")
    total_entropy = entropy(data, target_attr)

    splits = split_data(data, attr)
    total = len(data)

    weighted_entropy = 0

    for value, subset in splits.items():
        print(f"\nSubset where {attr} = {value}")
        subset_entropy = entropy(subset, target_attr)
        weight = len(subset) / total
        weighted_entropy += weight * subset_entropy
        print(f"Weighted Entropy for {value} = {weight} * {subset_entropy}")

    gain = total_entropy - weighted_entropy
    print(f"Information Gain({attr}) = {gain}")
    return gain


# -----------------------------
# Gini Gain
# -----------------------------
def gini_gain(data, attr, target_attr):
    print(f"\nCalculating Gini Gain for attribute: {attr}")
    total_gini = gini_index(data, target_attr)

    splits = split_data(data, attr)
    total = len(data)

    weighted_gini = 0

    for value, subset in splits.items():
        print(f"\nSubset where {attr} = {value}")
        subset_gini = gini_index(subset, target_attr)
        weight = len(subset) / total
        weighted_gini += weight * subset_gini
        print(f"Weighted Gini for {value} = {weight} * {subset_gini}")

    gain = total_gini - weighted_gini
    print(f"Gini Gain({attr}) = {gain}")
    return gain


# -----------------------------
# Best Attribute Selection
# -----------------------------
def best_attribute(data, attributes, target_attr, method):
    best_attr = None
    best_score = -1

    print("\nEvaluating Best Attribute...\n")

    for attr in attributes:
        if method == "entropy":
            score = information_gain(data, attr, target_attr)
        else:
            score = gini_gain(data, attr, target_attr)

        print(f"Score for {attr} = {score}\n")

        if score > best_score:
            best_score = score
            best_attr = attr

    print(f"Best Attribute Selected: {best_attr}\n")
    return best_attr


# -----------------------------
# Build Decision Tree
# -----------------------------
def build_tree(data, attributes, target_attr, depth=0, max_depth=3, method="entropy"):
    counts = Counter([row[target_attr] for row in data])

    # Pure node
    if len(counts) == 1:
        print("Pure Node Found:", list(counts.keys())[0])
        return list(counts.keys())[0]

    # Stop condition
    if not attributes or depth == max_depth:
        majority = counts.most_common(1)[0][0]
        print("Max depth reached. Majority Class:", majority)
        return majority

    best_attr = best_attribute(data, attributes, target_attr, method)
    tree = {best_attr: {}}

    splits = split_data(data, best_attr)
    remaining_attrs = [a for a in attributes if a != best_attr]

    for value, subset in splits.items():
        print(f"\nBuilding subtree for {best_attr} = {value}")
        subtree = build_tree(subset, remaining_attrs, target_attr, depth+1, max_depth, method)
        tree[best_attr][value] = subtree

    return tree


# -----------------------------
# Print Tree
# -----------------------------
def print_tree(tree, indent=""):
    if not isinstance(tree, dict):
        print(indent + "-> " + tree)
        return

    for attr, branches in tree.items():
        for value, subtree in branches.items():
            print(indent + f"{attr} = {value}")
            print_tree(subtree, indent + "   ")


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":

    print("1. Read from CSV file")
    print("2. Manual Input")
    choice = int(input("Enter your choice: "))

    if choice == 1:
        filename = input("Enter CSV filename: ")
        headers, data = read_data(filename)
    else:
        headers, data = manual_input()

    print("\n1. Information Gain (Entropy)")
    print("2. Gini Index")
    method_choice = int(input("Choose splitting method: "))

    method = "entropy" if method_choice == 1 else "gini"

    target_attribute = headers[-1]
    attributes = headers[:-1]

    print("\nBuilding Decision Tree...\n")

    tree = build_tree(data, attributes, target_attribute, method=method)

    print("\nFinal Decision Tree:\n")
    print_tree(tree)
