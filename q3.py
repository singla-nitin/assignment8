import itertools
from collections import defaultdict
import matplotlib.pyplot as plt


def load_dataset(filepath):
    with open(filepath, 'r', encoding='ISO-8859-1') as file:  
        transactions = [line.strip().split() for line in file]
    return transactions


def get_support_counts(transactions, itemsets):
    support_counts = defaultdict(int)
    for transaction in transactions:
        transaction_set = set(transaction)
        for itemset in itemsets:
            if itemset.issubset(transaction_set):
                support_counts[itemset] += 1
    return support_counts


def generate_candidates(frequent_itemsets, k):
    candidates = []
    frequent_items = list(frequent_itemsets.keys())
    for i in range(len(frequent_items)):
        for j in range(i + 1, len(frequent_items)):
            candidate = frequent_items[i].union(frequent_items[j])
            if len(candidate) == k:
                candidates.append(candidate)
    return set(candidates)


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

def generate_association_rules(frequent_itemsets, min_confidence, transactions):
    rules = []
    transaction_count = len(transactions)

  
    support_count = {itemset: count for itemset, count in frequent_itemsets.items()}

   
    for itemset in frequent_itemsets.keys():
        if len(itemset) < 2:
            continue
       
        for i in range(1, len(itemset)):
            for lhs in itertools.combinations(itemset, i):
                lhs = frozenset(lhs)
                rhs = itemset - lhs
                if rhs:
                   
                    confidence = support_count[itemset] / support_count[lhs]
                    if confidence >= min_confidence:
                        rule = (lhs, rhs, confidence)
                        rules.append(rule)
    return rules


def experiment_with_support_and_confidence(filepath, min_support_counts, min_confidence_values):
    transactions = load_dataset(filepath)

   
    support_pattern_counts = []
    confidence_rule_counts = {min_conf: [] for min_conf in min_confidence_values}

   
    for min_support in min_support_counts:
        frequent_itemsets = apriori(transactions, min_support)
        support_pattern_counts.append(len(frequent_itemsets))

       
        for min_confidence in min_confidence_values:
            rules = generate_association_rules(frequent_itemsets, min_confidence, transactions)
            confidence_rule_counts[min_confidence].append(len(rules))

    return support_pattern_counts, confidence_rule_counts


filepath = 'your file path'  
min_support_counts = [500, 1000, 1500, 2000]  
min_confidence_values = [0.4, 0.5, 0.6, 0.7]  


support_pattern_counts, confidence_rule_counts = experiment_with_support_and_confidence(filepath, min_support_counts, min_confidence_values)


plt.figure(figsize=(12, 5))


plt.subplot(1, 2, 1)
plt.plot(min_support_counts, support_pattern_counts, marker='o', color='b', label='Frequent Patterns')
plt.xlabel('Minimum Support Count')
plt.ylabel('Number of Frequent Patterns')
plt.title('Frequent Patterns vs Minimum Support Count')
plt.legend()


plt.subplot(1, 2, 2)
for min_confidence, rule_counts in confidence_rule_counts.items():
    plt.plot(min_support_counts, rule_counts, marker='o', label=f'Min Confidence = {min_confidence}')
plt.xlabel('Minimum Support Count')
plt.ylabel('Number of Association Rules')
plt.title('Association Rules vs Minimum Support Count')
plt.legend()

plt.tight_layout()
plt.show()
