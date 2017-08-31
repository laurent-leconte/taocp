"""Implementation of the permutation algorithms (chapter 1.3.3).
To stick to the original text, a permutation is represented as a list of tuples of numbers from 1 to n.
So for instance `[(1, 2, 3),(4,6)]` corresponds to (a b c)(d f) using Knuth's notation.
"""

def permutation_product_A(perms):
    """Implement algorithm B of chapter 1.3.3

    :param perms: the list of permutations (themselves a list of cycles) to multiply
    :return: The product of the permutations in normalized form
    """
    if len(perms) == 0:
        #input is the identity permutation - return id
        return []
    # Start by flattening the input to a list of cycles if necessary
    cycles = flatten_permutations(perms)
    # First pass (step A1). Tag left parens and replace right parens by tagged first element of cycle.
    # Tagging is done by negating the input. Left parens are actually not tracked, as they don't come into play.
    symbols = []
    for cycle in cycles:
        symbols.extend(cycle)
        symbols.append(- cycle[0])
    result = []
    n = len(symbols)
    closed = True
    #main loop : we will go over the symbols table, outputting a new symbol after each loop
    while True:
        idx = 0
        if closed:
            #step A2 : find first untagged element and start a new cycle
            while symbols[idx] < 0:
                idx += 1
                if idx == n:
                    #all elements are tagged: we're done
                    return sorted(result)
            # open new cycle, add current element and tag it.
            start = symbols[idx]
            current_cycle = [start]
            symbols[idx] = -start
            # step A3 : set current to next value.
            idx += 1
            current = abs(symbols[idx])
            idx += 1
        #A4 : now go through the rest of the symbols, tagging and updating each time we find a symbol equal to current
        while idx < n:
            if abs(symbols[idx]) == current:
                #tag symbol and do A3
                symbols[idx] = - abs(symbols[idx])
                current = abs(symbols[idx + 1])
                idx += 1
            idx += 1
        # We've reach the end of the symbols
        if current != start:
            #step A5: add current result to current cycle, start over the scan (A4) from the beginning
            current_cycle.append(current)
            closed = False
        else:
            #step A6 : close current cycle and add it to the result. If cycle length is one, ignore it
            if len(current_cycle) > 1:
                result.append(normalized_tuple(current_cycle))
            closed = True

def permutation_product_B(perms):
    """Implement algorithm B of chapter 1.3.3

    :param perms: the list of permutations (themselves a list of cycles) to multiply
    :return: The product of the permutations in normalized form
    """
    if len(perms) == 0:
        # Input is the identity permutation - return id
        return []
    # Start by flattening the input to a list of cycles if necessary
    cycles = flatten_permutations(perms)

    # Step B1: find n and init T.
    n = max([max(cycle) for cycle in cycles])
    T = list(range(n+1))
    # Step B2 : iterate over the input from right to left
    for cycle in reversed(cycles):
        # Step B2 - input is ')'
        # Here, T[0] is used to hold Z
        T[0] = 0
        for i in reversed(cycle):
            # Step B3 : switch Z and T[i]
            T[0], T[i] = T[i], T[0]
            if T[i] == 0:
                j = i
        # Step B4
        T[j] = T[0]
    # end of main algorithm. Now translate the result in cycle form.
    result = []
    T[0] = 0
    while True:
        # find first untagged element
        idx = 0
        while idx <= n and T[idx] <= 0:
            idx += 1
        if idx > n:
            # no more untagged elements, return result
            return sorted(result)
        # start new cycle
        cycle = []
        while T[idx] > 0:
            # add current element to cycle
            cycle.append(idx)
            # tag element and go to next one
            j = T[idx]
            T[idx] = 0
            idx = j
        # end of cycle, add it to result if it is not a singleton
        if len(cycle) > 1:
            result.append(normalized_tuple(cycle))

def normalized_tuple(cycle):
    """Return a normalized version (starting from the smallest element) of the cycle
    :param cycle: The cycle (in list form) to normalize
    :return: A tuple representing the cycle
    """
    min_val = cycle[0]
    min_idx = 0
    for idx in range(1, len(cycle)):
        if cycle[idx] < min_val:
            min_val = cycle[idx]
            min_idx = idx
    return tuple(cycle[min_idx:] + cycle[:min_idx])

def flatten_permutations(perms):
    if isinstance(perms[0], list):
        return [cycle for perm in perms for cycle in perm]
    else:
        return perms

if __name__ == '__main__':
    perm1 = [(1, 2, 3),(4,6)]
    inv_perm1 = [(4,6),(2,1,3)]
    perm2 = [(3,5),(1,4)]
    perms = [perm1, perm2]
    knuth = [(1, 3, 6, 7), (2, 3, 4), (1, 5, 4), (6, 1, 4, 5), (2, 7, 6, 1, 5)]
    print(permutation_product_B(knuth))
    print(permutation_product_A(knuth))
    print(permutation_product_B([(1,)]))
    print(permutation_product_B(perm1 + inv_perm1))

