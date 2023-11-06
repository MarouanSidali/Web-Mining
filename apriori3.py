
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import pandas as pd

# Load your data from a CSV file
df = pd.read_csv('Market_Basket_Optimisation.csv', header=None)

# Convert the data to a list of transactions
transactions = []
for index, row in df.iterrows():
    transactions.append([str(item) for item in row if pd.notna(item)])

# Encode the data into a one-hot format
oht = pd.get_dummies(pd.DataFrame(transactions), prefix='', prefix_sep='')

# Use Apriori to find frequent itemsets with a minimum support of 0.2
frequent_itemsets = apriori(oht, min_support=0.02, use_colnames=True)  # Adjust the min_support value


# Generate association rules with a minimum confidence of 0.7
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.3)

# Display frequent itemsets and association rules
print("Frequent Itemsets:")
print(frequent_itemsets)

print("\nAssociation Rules:")
print(rules)