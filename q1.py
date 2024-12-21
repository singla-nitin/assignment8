import itertools
from collections import defaultdict


def load_dataset(filepath):
    """
    Load transactions from a file where each line is a transaction with item IDs separated by spaces.
    """
    with open(filepath, 'r', encoding='ISO-8859-1') as file: 
        transactions = [line.strip().split() for line in file]
    return transactions


def get_support_counts(transactions, itemsets):
    """
    Calculate the support count for each itemset in the list of transactions.
    """
    support_counts = defaultdict(int)
    for transaction in transactions:
        transaction_set = set(transaction)
        for itemset in itemsets:
            if itemset.issubset(transaction_set):
                support_counts[itemset] += 1
    return support_counts


def generate_candidates(frequent_itemsets, k):
    """
    Generate candidate itemsets of size k based on frequent itemsets of size k-1.
    """
    candidates = []
    frequent_items = list(frequent_itemsets.keys())
    for i in range(len(frequent_items)):
        for j in range(i + 1, len(frequent_items)):
            candidate = frequent_items[i].union(frequent_items[j])
            if len(candidate) == k:
                candidates.append(candidate)
    return set(candidates)


def apriori(transactions, min_support_count):
    """
    Run the Apriori algorithm on transactions with a specified minimum support count.
    """
    
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


def find_frequent_patterns(filepath, min_support_counts):
    """
    Run the Apriori algorithm for each minimum support count in min_support_counts and return results.
    """
    transactions = load_dataset(filepath)
    results = {}
    for min_support in min_support_counts:
        print(f"Running Apriori with minimum support count = {min_support}")
        frequent_itemsets = apriori(transactions, min_support)
        results[min_support] = frequent_itemsets
        print(f"Found {len(frequent_itemsets)} frequent itemsets with min support {min_support}")
    return results


filepath = 'your file path'

min_support_counts = [100, 500, 1000, 1500]


results = find_frequent_patterns(filepath, min_support_counts)


for min_support, itemsets in results.items():
    print(f"\nMinimum Support: {min_support}")
    for itemset, count in itemsets.items():
        print(f"Itemset: {set(itemset)}, Support Count: {count}")
