import itertools
from collections import defaultdict


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


def find_association_rules(filepath, min_support_count, min_confidence_values):
    transactions = load_dataset(filepath)
    
    frequent_itemsets = apriori(transactions, min_support_count)

   
    results = {}
    for min_confidence in min_confidence_values:
        print(f"Generating rules with minimum confidence = {min_confidence}")
        rules = generate_association_rules(frequent_itemsets, min_confidence, transactions)
        results[min_confidence] = rules
        print(f"Found {len(rules)} rules with min confidence {min_confidence}")
    return results


filepath = 'your file path' 
min_support_count = 1000  
min_confidence_values = [0.5, 0.6, 0.7]  


association_rules_results = find_association_rules(filepath, min_support_count, min_confidence_values)


for min_confidence, rules in association_rules_results.items():
    print(f"\nMinimum Confidence: {min_confidence}")
    for lhs, rhs, confidence in rules:
        print(f"Rule: {set(lhs)} => {set(rhs)}, Confidence: {confidence:.2f}")
