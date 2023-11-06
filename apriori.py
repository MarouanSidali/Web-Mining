"""
Description: Python implementation of the Apriori Algorithm
Author: Ahmed Atya
ID: 20180013
Group: IS_S2
"""

from itertools import chain, combinations
from collections import defaultdict


def subsets(arr):
    return chain(*[combinations(arr, i + 1) for i, item in enumerate(arr)])


def getItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet):
    _itemSet = set()
    _localSet = defaultdict(int)

    for item in itemSet:
        for transaction in transactionList:
            if item.issubset(transaction):
                freqSet[item] += 1
                _localSet[item] += 1

    for item, count in _localSet.items():
        support = count / len(transactionList)
        if support >= minSupport:
            _itemSet.add(item)

    return _itemSet


def joinSet(itemSet, length):
    """
       (A,B)
       (B,*)
       (A,*)
    """
    return set(
        [i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length]
    )


def getItemSetAndTransactionList(data_iterator):
    transactionList = list()  # contains all transactions
    itemSet = set()  # contains all unique items
    for record in data_iterator:
        transaction = frozenset(record)
        transactionList.append(transaction)
        for item in transaction:
            itemSet.add(frozenset([item]))  # Generate 1-itemSets

    return itemSet, transactionList


def runApriori(data_iterator, minSupport, minConfidence):
    """
     - allItems (tuple, support)
     - AssociationRules ((prev-tuple, post-tuple), confidence)
    """
    itemSet, transactionList = getItemSetAndTransactionList(data_iterator)  # Generate 1-itemSets

    freqSet = defaultdict(int)
    largeSet = dict()

    oneCSet = getItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet)  # Filter based on support threshold

    currentLSet = oneCSet
    k = 2
    while currentLSet != set([]):
        largeSet[k - 1] = currentLSet
        currentLSet = joinSet(currentLSet, k)
        currentCSet = getItemsWithMinSupport(
            currentLSet, transactionList, minSupport, freqSet
        )
        currentLSet = currentCSet
        k = k + 1

    def getSupport(item):
        return float(freqSet[item]) / len(transactionList)

    """ Largest Set =  {1: {frozenset({'Cheese'}), frozenset({'Pencil'}), 2: {frozenset({'Bread'}), frozenset({'Pencil'})} """
    allItems = []
    for key, value in largeSet.items():
        allItems.extend([(tuple(item), getSupport(item)) for item in value])

    AssociationRules = []
    for key, value in list(largeSet.items())[1:]:
        """
        item = {'Milk', 'Bread'}
        _subsets = {'Milk'}, {'Bread'}, {'Milk', 'Bread'}
        remain = {'Bread'}
        remain = {'Milk'}
        remain = {}
        """
        for item in value:
            _subsets = map(frozenset, [x for x in subsets(item)])
            for element in _subsets:
                remain = item.difference(element)
                if len(remain) > 0:
                    confidence = getSupport(item) / getSupport(element)
                    if confidence >= minConfidence:
                        AssociationRules.append(((tuple(element), tuple(remain)), confidence))
    return allItems, AssociationRules


def printResults(items, rules):
    print("***************** ITEMS *********************")
    for item, support in sorted(items, key=lambda x: x[1]):
        print("item: %s = %.5f" % (str(item), support))

    print("***************** RULES *********************")
    for rule, confidence in sorted(rules, key=lambda x: x[1]):
        pre, post = rule
        print("Rule: %s >>>> %s = %.5f" % (str(pre), str(post), confidence))


def readFile(file_name):
    with open(file_name, "r") as file_iter:
        for line in file_iter:
            line = line.strip().rstrip(",")
            record = frozenset(line.split(",")[1:])
            yield record


if __name__ == "__main__":
    file_name = "Market_Basket_Optimisation.csv"
    inFile = readFile(file_name)

    print("Enter Min support value: ")
    minSupportThreshold = float(input())  # 0.2
    print("Enter Min confidence value: ")
    minConfidenceThreshold = float(input())  # 0.6

    items, rules = runApriori(inFile, minSupportThreshold, minConfidenceThreshold)

    printResults(items, rules)