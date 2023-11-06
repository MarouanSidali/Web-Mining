# Load the transactions from the dataset
from itertools import combinations

def load_data(filename):
    data = []
    with open(filename, 'r') as file:
        for line in file:
            transaction = line.strip().split(',')
            data.append(transaction)
    return data

# Generate frequent itemsets of size 1
def get_frequent_1_itemsets(data, min_support):
    item_counts = {}
    for transaction in data:
        for item in transaction:
            if item in item_counts:
                item_counts[item] += 1
            else:
                item_counts[item] = 1

    frequent_1_itemsets = {item: support for item, support in item_counts.items() if support >= min_support}
    return frequent_1_itemsets

# Generate candidate itemsets of size k from frequent itemsets of size k-1
def generate_candidates(prev_frequent_itemsets, k):
    candidates = set()
    for itemset1 in prev_frequent_itemsets:
        for itemset2 in prev_frequent_itemsets:
            itemset1 = set(itemset1)
            itemset2 = set(itemset2)
            if len(itemset1.union(itemset2)) == k:
                candidates.add(tuple(sorted(itemset1.union(itemset2))))
    return candidates

# Prune candidate itemsets that have infrequent subsets
def prune_candidates(candidates, prev_frequent_itemsets, k):
    pruned_candidates = set()
    for candidate in candidates:
        is_frequent = True
        subsets = [set(item) for item in combinations(candidate, k - 1)]
        for subset in subsets:
            if tuple(sorted(subset)) not in prev_frequent_itemsets:
                is_frequent = False
                break
        if is_frequent:
            pruned_candidates.add(candidate)
    return pruned_candidates

# Generate frequent itemsets of size k
def get_frequent_k_itemsets(data, prev_frequent_itemsets, k, min_support):
    candidates = generate_candidates(prev_frequent_itemsets, k)
    pruned_candidates = prune_candidates(candidates, prev_frequent_itemsets, k)
    item_counts = {tuple(itemset): 0 for itemset in pruned_candidates}

    for transaction in data:
        for candidate in pruned_candidates:
            if set(candidate).issubset(transaction):
                item_counts[candidate] += 1

    frequent_k_itemsets = {itemset: support for itemset, support in item_counts.items() if support >= min_support}
    return frequent_k_itemsets

# Generate association rules from frequent itemsets
def generate_association_rules(frequent_itemsets, min_confidence):
    rules = []
    for itemset, support in frequent_itemsets.items():
        if len(itemset) >= 2:
            for i in range(1, len(itemset)):
                antecedent = tuple(sorted(list(itemset)[:i]))
                consequent = tuple(sorted(list(itemset)[i:]))
                confidence = support / frequent_itemsets[antecedent]
                if confidence >= min_confidence:
                    rules.append((antecedent, consequent, confidence))
    return rules

# Main Apriori algorithm
def apriori(data, min_support, min_confidence):
    frequent_itemsets = {}
    k = 1

    frequent_1_itemsets = get_frequent_1_itemsets(data, min_support)
    frequent_itemsets.update(frequent_1_itemsets)

    while frequent_itemsets:
        k += 1
        frequent_k_itemsets = get_frequent_k_itemsets(data, frequent_itemsets.keys(), k, min_support)
        if frequent_k_itemsets:
            frequent_itemsets.update(frequent_k_itemsets)

    association_rules = generate_association_rules(frequent_itemsets, min_confidence)
    return frequent_itemsets, association_rules

# Load the dataset
data = load_data('Market_Basket_Optimisation.csv')

# Set minimum support and confidence thresholds
min_support = 0.01
min_confidence = 0.3

# Run Apriori algorithm
frequent_itemsets, association_rules = apriori(data, min_support, min_confidence)

# Display frequent itemsets
print("Frequent Itemsets:")
for itemset, support in frequent_itemsets.items():
    print(f"{itemset}: {support}")

# Display association rules
print("\nAssociation Rules:")
for rule in association_rules:
    antecedent, consequent, confidence = rule
    print(f"{antecedent} => {consequent} (Confidence: {confidence})")






