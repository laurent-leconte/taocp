"""Implementation of the permutation algorithms (chapter 1.3.3).
To stick to the original text, a permutation is represented as a list of tuples of numbers from 1 to n.
So for instance `[(1, 2, 3),(4,6)]` corresponds to (a b c)(d f) using Knuth's notation.
"""

def permutation_product(perms):
    """Implement Algorithm A of chapter 1.3.3.
    Arg:
        perms: a list of cycles to multiply
    """
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
                    return result
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
                result.append(tuple(current_cycle))
            closed = True

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
    print(permutation_product(knuth))
    print(permutation_product(perm1 + inv_perm1))

