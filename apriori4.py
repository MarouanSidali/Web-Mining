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

# Generate candidate itemsets
def generate_candidate_itemsets(level_k, level_frequent_itemsets):
    return {itemset1.union(itemset2) for itemset1 in level_frequent_itemsets for itemset2 in level_frequent_itemsets 
            if len(itemset1.union(itemset2)) == level_k}

# Returns frequent itemsets
def generate_frequent_itemsets(dataset, candidate_itemsets):
    counter = defaultdict(int)
    for transaction in dataset:
        for itemset in candidate_itemsets:
            if itemset.issubset(transaction):
                counter[itemset] += 1
    return {itemset: frequency for itemset, frequency in counter.items() if frequency/len(dataset) >= min_support}

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
for k in range(1, 20):
    if k == 1:
        candidate_itemsets = {frozenset([item]) for transaction in dataset for item in transaction}
    else:
        candidate_itemsets = generate_candidate_itemsets(k, frequent_itemsets[k-1])
    frequent_itemsets[k] = generate_frequent_itemsets(dataset, candidate_itemsets)
    if not frequent_itemsets[k]:
        del frequent_itemsets[k]
        break

# Print the frequent itemsets
for level, itemsets in frequent_itemsets.items():
    print(f"Level {level}:")
    for itemset, frequency in itemsets.items():
        support = frequency / len(dataset)
        print(f"Itemset: {itemset}, Support: {support: .5f}")

# Flatten the frequent_itemsets dictionary
flat_frequent_itemsets = {itemset: frequency for level_itemsets in frequent_itemsets.values() for itemset, frequency in level_itemsets.items()}

# Generate association rules
rules = generate_rules(flat_frequent_itemsets, min_confidence)
# Print the generated rules
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

