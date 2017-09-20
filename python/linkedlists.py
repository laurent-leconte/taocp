"""Implementation of the linked list  and circular lists algorithms (chapter 2.2.3 and 2.2.4).

"""

import itertools

def topological_sort(relations):
    """Implement algorithm T of chapter 2.2.3.

    In this implementation the linked lists are actually replaced by lists.
    This does not depart significantly from the spirit of the original as we only use the `pop` and `append` methods.

    :param relations: a list of pairs representing the relations between objects
    :return: the list of objects in sorted order
    :raises:
    """
    # step T1 : initialize N, count and top
    # as usual, we will keep the 1-indexing from Knuth and ignore the first value of the lists.
    n = max([max(e) for e in relations])
    N = n
    count = [0]*(n+1)
    top = []
    # Can't use top = [[]]*(n+1) or we would modify all elements every time we push to one of them (shallow copy)
    for i in range(n+1):
        top.append([])
    # step T2 / T3 : ingest relations
    for (j,k) in relations:
        count[k] += 1
        top[j].append(k)
    # step T4
    qlink = []
    for k in range(1, n+1):
        if count[k] == 0:
            qlink.append(k)
    result = []
    # loop on queue
    while len(qlink) > 0:
        # Step T5 + T7
        f = qlink.pop()
        result.append(f)
        N -= 1
        # T6 : erase relations
        while len(top[f]) > 0:
            suc = top[f].pop()
            count[suc] -= 1
            if count[suc] == 0:
                qlink.append(suc)
    # step T8
    if N == 0:
        return result
    else:
        raise ValueError("Loop in input relations")


def polynomial_addition(p, q):
    """Implement algorithm A of chapter 2.2.4.

    This algorithm does not actually make use of circular lists, as each list is traversed only once.
    Nonetheless, the implementation uses the `cycle` method from itertools lists to emulate a circular list (this frees
    us from the temptation to test for the end of the list to terminate the algorithm, and prepares us for the
    multiplication algorithm).
    Each polynomial is described as a list of nested tuples of the form (coef, (a, b, c)).
    The last element of each polynomial is always (0, (0, 0, -1)).

    :param p: the first polynomial to add
    :param q: the second polynomial to add
    :return: the sum of p and q as a new list (note that this is different from the original algorithm
    which adds to q in place.)
    """
    result = []
    circular_p = itertools.cycle(p)
    circular_q = itertools.cycle(q)
    # step A1. P and Q are used to denote the value of the current element of p and q
    P = next(circular_p)
    Q = next(circular_q)
    special = (0, 0, -1)

    def coef(X):
        return X[0]

    def abc(X):
        return X[1]
    # loop over p and q while the special node hasn't been reached (exit case of step A3)
    while abc(P) != special or abc(Q) != special :
        if abc(P) == abc(Q):
            # step A3
            c = coef(P) + coef(Q)
            if c != 0:
                result.append((c, abc(P)))
            P = next(circular_p)
            Q = next(circular_q)
        while abc(P) < abc(Q):
            # step A2
            result.append(Q)
            Q = next(circular_q)
        while abc(P) > abc(Q):
            # step A5
            result.append(P)
            P = next(circular_p)

    return result + [Q]

def polynomial_multiplication(p, m):
    """Implement algorithm M of chapter 2.2.4.

    As for addition, each polynomial is described as a list of nested tuples of the form (coef, (a, b, c)).
    The last element of each polynomial is always (0, (0, 0, -1)).

    :param p: first polynomial to multiply
    :param m: second polynomial to multiply
    :return: p*m as a new list (note that this is different from the original algorithm)
    """
    special = (0, 0, -1)
    result = []
    circular_p = itertools.cycle(p)
    print("start ", p, m)
    def coef(X):
        return X[0]

    def abc(X):
        return X[1]

    def add_abc(X, Y):
        a = abc(X)
        b = abc(Y)
        return tuple([e1 + e2 for (e1, e2) in zip(a, b)])

    # loop for step M1/M2
    for M in m:
        if abc(M) == (0, 0, -1):
            return result + [(0, special)]

        # initialize P and Q.
        P = next(circular_p)
        # poor man's version of circular lists : take the previous iteration's result, use it as a new list and store
        circular_q = iter(result.copy() + [(0, special)])
        Q = next(circular_q)
        result = []
        # same algorithm as for addition with a few changes
                while abc(P) != special or abc(Q) != special:
            if add_abc(P, M) == abc(Q):
                # step A3/M2. No need to check that abc(P) > -1 as this is always true in this branch
                c = coef(P)*coef(M) + coef(Q)
                if c != 0:
                    print("appending from A3 ", (c, abc(Q)))
                    result.append((c, abc(Q)))
                P = next(circular_p)
                Q = next(circular_q)
            if abc(P) > special:
                while add_abc(P, M) < abc(Q):
                    # step A2. # The while condition is probably not enough to cover the M2 check
                    print("appending from A2a ", Q)
                    result.append(Q)
                    Q = next(circular_q)
            else:
                while abc(Q) > special:
                    print("appending from A2b ", Q)
                    result.append(Q)
                    Q = next(circular_q)
            while abc(P) > special and add_abc(P, M) > abc(Q):
                # step A5
                X = (coef(P)*coef(M), add_abc(P, M))
                print("appending from A5 ", X)
                result.append(X)
                P = next(circular_p)

        #result.append((0, special))


if __name__ == '__main__':
    relations = [(9, 2), (3, 7), (7, 5), (5, 8), (8, 6), (4, 6), (1, 3), (7, 4), (9, 5), (2, 8)]
    #print(topological_sort(relations))
    zero = [(0, (0, 0, -1))]
    p = [(1, (1, 0, 0)), (1, (0, 1, 0)), (1, (0, 0, 1))] + zero
    print(polynomial_addition(p, zero))