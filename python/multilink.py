"""Implementation of the "Cobol compiler" algorithms from chapter 2.4.

"""

class DataElement(object):
    """ Simple storage class to represent a Data Table row

    """
    __slots__ = ('prev', 'parent', 'name', 'child', 'sib', 'key')

    def __init__(self, **kwargs):
        for e in self.__slots__:
            setattr(self, e, None)
        for (k, v) in kwargs.items():
            if k in self.__slots__:
                setattr(self, k, v)

    def __str__(self):
        return str(self.key)

    def __repr__(self):
        items = ('{}={}'.format(k, str(getattr(self, k))) for k in self.__slots__)
        return ', '.join(items)


def build_data_table(input_sequence):
    """ Implementation of algorithm A """
    data_table = {}
    symbol_table = {}
    # the stack will hold "pointers" to data elements (key in the data_table corresponding to the DataElement object)
    stack = [(0, None)]
    # A2 loop
    for (L, P) in input_sequence:
        # A3
        # PREV(Q) <- LINK(P)
        prev = symbol_table.get(P, None)
        # LINK(P) <- Q
        link = "%s%d" % (P, L)
        symbol_table[P] = link
        # add to symbol table
        Q = DataElement(name=P, prev=prev, key=link)
        data_table[link] = Q
        (L1, P1) = stack[-1]
        if L1 < L:
            # step A4 (no need for a pointer to the first entry of the data table)
            if P1 is not None:
                data_table[P1].child = Q.key
        else:
            # step A5
            while L1 > L:
                stack.pop()
                (L1, P1) = stack[-1]
            if L1 < L:
                raise ValueError("Mixed numbers on the same level")
            else:
                # L1 == L. Set sibling
                data_table[P1].sib = Q.key
                stack.pop()
                (L1, P1) = stack[-1]
        # step A6
        Q.parent = P1
        Q.child = None
        Q.sib = None
        stack.append((L, Q.key))
    return symbol_table, data_table




if __name__ == '__main__':
    sequence = ((1, 'A'), (3, 'B'), (7, 'C'), (7, 'D'), (3,'E'), (3, 'F'), (4, 'G'), (1, 'H'),
                (5, 'F'), (8, 'G'), (5, 'B'), (5, 'C'), (9, 'E'), (9, 'D'), (9, 'G'))
    s, d = build_data_table(sequence)
    print(s)
    print(d)
