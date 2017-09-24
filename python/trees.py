class BTree(object):

    def __init__(self, value=None, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        if self.is_leaf:
            res = "(%s)" % repr(self.value)
        else:
            if self.left is None:
                left_repr = "()"
            else:
                left_repr = repr(self.left)
            if self.right is None:
                right_repr = "()"
            else:
                right_repr = repr(self.right)
            res = "(%s %s %s)" % (left_repr, repr(self.value), right_repr)
        return res

    @property
    def is_leaf(self):
        return self.left is None and self.right is None


def in_order(t):
    res = []
    p = t
    a = []
    while p is not None:
        a.append(p)
        p = p.left
    while len(a) > 0:
        p = a.pop()
        res.append(p.value)
        p = p.right
        while p is not None:
            a.append(p)
            p = p.left
    return res

if __name__ == '__main__':
    l = BTree("B", BTree("D"))
    f = BTree("F", BTree("H"), BTree("J"))
    r = BTree("C", BTree("E", None, BTree("G")), f)
    t = BTree("A", l, r)
    print(t)
    print(in_order(t))