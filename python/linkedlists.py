"""Implementation of the linked list algorithms (chapter 2.2.3), in particular the topological sort.

"""

def topological_sort(relations):
    """Implement algorithm T of chapter 2.2.3. In this implementation the linked lists are actually replaced by lists.
    This does not depart significantly from the spirit of the original as we only use the `pop` and `append` methods.

    :param relations: a list of pairs representing the relations between objects
    :return: the list of objects in sorted order
    :raises:
    """
    #step T1 : initialize N, count and top
    #as usual, we will keep the 1-indexing from Knuth and ignore the first value of the lists.
    n = max([max(e) for e in relations])
    N = n
    count = [0]*(n+1)
    top = []
    #Can't use top = [[]]*(n+1) or we would modify all elements every time we push to one of them (shallow copy)
    for i in range(n+1):
        top.append([])
    #step T2 / T3 : ingest relations
    for (j,k) in relations:
        count[k] += 1
        top[j].append(k)
    #step T4
    qlink = []
    for k in range(1, n+1):
        if count[k] == 0:
            qlink.append(k)
    result = []
    #loop on queue
    while len(qlink) > 0:
        #Step T5 + T7
        f = qlink.pop()
        result.append(f)
        N -= 1
        #T6 : erase relations
        while len(top[f]) > 0:
            suc = top[f].pop()
            count[suc] -= 1
            if count[suc] == 0:
                qlink.append(suc)
    #step T8
    if N == 0:
        return result
    else:
        raise ValueError("Loop in input relations")

if __name__ == '__main__':
    relations = [(9, 2), (3, 7), (7, 5), (5, 8), (8, 6), (4, 6), (1, 3), (7, 4), (9, 5), (2, 8)]
    print(topological_sort(relations))