import csv
from collections import defaultdict
from itertools import combinations
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load data from CSV
def load_data(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data

def generate_candidate_itemsets(level_k, level_frequent_itemsets):
    # Initialize an empty set to store the candidate itemsets
    candidate_itemsets = set()

    # Iterate over all pairs of itemsets in level_frequent_itemsets
    for itemset1 in level_frequent_itemsets:
        for itemset2 in level_frequent_itemsets:
            # Take the union of itemset1 and itemset2
            union = itemset1.union(itemset2)

            # If the size of the union is equal to level_k, add it to candidate_itemsets
            if len(union) == level_k:
                candidate_itemsets.add(union)

    # Return the set of candidate itemsets
    return candidate_itemsets

# Returns frequent itemsets
def generate_frequent_itemsets(transactions, candidate_itemsets):
    # Initialize a dictionary to count the occurrences of each itemset
    itemset_counts = defaultdict(int)

    # Count the occurrences of each itemset in the transactions
    for transaction in transactions:
        for itemset in candidate_itemsets:
            if itemset.issubset(transaction):
                itemset_counts[itemset] += 1

    # Calculate the total number of transactions
    total_transactions = len(transactions)

    # Generate the frequent itemsets by filtering out itemsets with support less than min_support
    frequent_itemsets = {
        itemset: count
        for itemset, count in itemset_counts.items()
        if count / total_transactions >= min_support
    }

    return frequent_itemsets

# Generate association rules
def generate_rules(frequent_itemsets, min_confidence):
    rules = []
    for itemset, frequency in frequent_itemsets.items():
        for i in range(1, len(itemset)):
            for subset in combinations(itemset, i):
                subset = frozenset(subset)
                if subset in frequent_itemsets:
                    subset_frequency = frequent_itemsets[subset]
                    confidence = frequency / subset_frequency
                    if confidence >= min_confidence:
                        rules.append((set(subset), itemset.difference(subset), confidence))
    return rules

# Parameters
min_support = 0.02
min_confidence = 0.3

# Load data
dataset = load_data('Market_Basket_Optimisation.csv')

# Apriori algorithm
frequent_itemsets = dict()
for k in range(1, 10):
    if k == 1:
        candidate_itemsets = {frozenset([item]) for transaction in dataset for item in transaction}
    else:
        candidate_itemsets = generate_candidate_itemsets(k, frequent_itemsets[k-1])
    frequent_itemsets[k] = generate_frequent_itemsets(dataset, candidate_itemsets)
    if not frequent_itemsets[k]:
        del frequent_itemsets[k]
        break

# Print the frequent itemsets
print("\n********************Frequent Itemsets********************\n")

for level, itemsets in frequent_itemsets.items():
    print(f"Level {level}:")
    for itemset, frequency in itemsets.items():
        support = frequency / len(dataset)
        print(f"Itemset: {itemset}, Support: {support: .5f}")

# Flatten the frequent_itemsets dictionary
# Initialize an empty dictionary
flat_frequent_itemsets = {}
print(frequent_itemsets)

# Iterate over each level of itemsets in the frequent_itemsets dictionary
for level_itemsets in frequent_itemsets.values():
    # Iterate over each itemset and its frequency
    for itemset, frequency in level_itemsets.items():
        # Add the itemset and its frequency to the flat_frequent_itemsets dictionary
        flat_frequent_itemsets[itemset] = frequency

# Generate association rules
rules = generate_rules(flat_frequent_itemsets, min_confidence)
# Print the generated rules
print(rules)
print("\n*********************Association Rules********************\n")
for rule in rules:
    print(f"{rule[0]} => {rule[1]}, confidence = {rule[2]: .5f}")
    

# # Prepare data for the heatmap
# antecedents = [str(rule[0]) for rule in rules]
# consequents = [str(rule[1]) for rule in rules]
# confidences = [rule[2] for rule in rules]
# data = pd.DataFrame({'antecedent': antecedents, 'consequent': consequents, 'confidence': confidences})

# # Pivot the data
# pivot_table = data.pivot(index='antecedent', columns='consequent', values='confidence')

# # Create heatmap
# plt.figure(figsize=(10, 10))
# sns.heatmap(pivot_table, cmap='YlGnBu')
# plt.title('Heatmap of Association Rules')
# plt.show()

