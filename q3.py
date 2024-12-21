import itertools
from collections import defaultdict
import matplotlib.pyplot as plt

# Load the dataset
def load_dataset(filepath):
    with open(filepath, 'r', encoding='ISO-8859-1') as file:  # Specify encoding to avoid Unicode errors
        transactions = [line.strip().split() for line in file]
    return transactions

# Get item support counts
def get_support_counts(transactions, itemsets):
    support_counts = defaultdict(int)
    for transaction in transactions:
        transaction_set = set(transaction)
        for itemset in itemsets:
            if itemset.issubset(transaction_set):
                support_counts[itemset] += 1
    return support_counts

# Generate candidate itemsets of size k
def generate_candidates(frequent_itemsets, k):
    candidates = []
    frequent_items = list(frequent_itemsets.keys())
    for i in range(len(frequent_items)):
        for j in range(i + 1, len(frequent_items)):
            candidate = frequent_items[i].union(frequent_items[j])
            if len(candidate) == k:
                candidates.append(candidate)
    return set(candidates)

# Apriori algorithm to find frequent itemsets
def apriori(transactions, min_support_count):
    single_items = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            single_items[frozenset([item])] += 1
    frequent_itemsets = {itemset: count for itemset, count in single_items.items() if count >= min_support_count}

    k = 2
    all_frequent_itemsets = frequent_itemsets.copy()
    while frequent_itemsets:
        candidates = generate_candidates(frequent_itemsets, k)
        candidate_support_counts = get_support_counts(transactions, candidates)
        frequent_itemsets = {itemset: count for itemset, count in candidate_support_counts.items() if count >= min_support_count}
        all_frequent_itemsets.update(frequent_itemsets)
        k += 1

    return all_frequent_itemsets

# Generate association rules from frequent itemsets
def generate_association_rules(frequent_itemsets, min_confidence, transactions):
    rules = []
    transaction_count = len(transactions)

    # Support count dictionary
    support_count = {itemset: count for itemset, count in frequent_itemsets.items()}

    # Iterate over all itemsets with size >= 2 to generate rules
    for itemset in frequent_itemsets.keys():
        if len(itemset) < 2:
            continue
        # For each itemset, try to split it into rule pairs: LHS => RHS
        for i in range(1, len(itemset)):
            for lhs in itertools.combinations(itemset, i):
                lhs = frozenset(lhs)
                rhs = itemset - lhs
                if rhs:
                    # Calculate confidence
                    confidence = support_count[itemset] / support_count[lhs]
                    if confidence >= min_confidence:
                        rule = (lhs, rhs, confidence)
                        rules.append(rule)
    return rules

# Experiment with different support counts and confidence levels
def experiment_with_support_and_confidence(filepath, min_support_counts, min_confidence_values):
    transactions = load_dataset(filepath)

    # Data storage for plotting
    support_pattern_counts = []
    confidence_rule_counts = {min_conf: [] for min_conf in min_confidence_values}

    # Find frequent itemsets for each support count
    for min_support in min_support_counts:
        frequent_itemsets = apriori(transactions, min_support)
        support_pattern_counts.append(len(frequent_itemsets))

        # Generate association rules for each confidence level
        for min_confidence in min_confidence_values:
            rules = generate_association_rules(frequent_itemsets, min_confidence, transactions)
            confidence_rule_counts[min_confidence].append(len(rules))

    return support_pattern_counts, confidence_rule_counts

# File path for retail dataset (update this path with the location of retail.txt on your system)
filepath = '/content/drive/MyDrive/Colab Notebooks/DATASETS/retail.txt'  # Replace with your dataset path
min_support_counts = [500, 1000, 1500, 2000]  # Minimum support thresholds for frequent itemsets
min_confidence_values = [0.4, 0.5, 0.6, 0.7]  # Varying confidence values

# Run the experiment and gather results
support_pattern_counts, confidence_rule_counts = experiment_with_support_and_confidence(filepath, min_support_counts, min_confidence_values)

# Plotting the number of frequent patterns for different support counts
plt.figure(figsize=(12, 5))

# Plot frequent patterns vs support count
plt.subplot(1, 2, 1)
plt.plot(min_support_counts, support_pattern_counts, marker='o', color='b', label='Frequent Patterns')
plt.xlabel('Minimum Support Count')
plt.ylabel('Number of Frequent Patterns')
plt.title('Frequent Patterns vs Minimum Support Count')
plt.legend()

# Plot association rules vs confidence for each support count
plt.subplot(1, 2, 2)
for min_confidence, rule_counts in confidence_rule_counts.items():
    plt.plot(min_support_counts, rule_counts, marker='o', label=f'Min Confidence = {min_confidence}')
plt.xlabel('Minimum Support Count')
plt.ylabel('Number of Association Rules')
plt.title('Association Rules vs Minimum Support Count')
plt.legend()

plt.tight_layout()
plt.show()
