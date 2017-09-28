import re


class ParseError(Exception):
    pass


class BTree(object):
    """Simple binary tree class.

    Some shortcomings: no check that children are actually binary tree.
    Needs a formal definition and management of empty trees.
    Parsing from string has not been tested robustly. Clunky `rec_repr` function.

    Do not use in real life!"""

    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


    def __repr__(self):
        return self.rec_repr()

    def rec_repr(self, prefix=''):
        if self.is_leaf:
            if self.value is None:
                res = '(%s)' % prefix
            else:
                res = "(%s%s)" % (prefix, str(self.value))
        else:
            if self.left is None:
                left_repr = "()"
            else:
                if prefix == '':
                    new_prefix = ''
                else:
                    new_prefix = prefix + '0'
                left_repr = self.left.rec_repr(new_prefix)
            if self.right is None:
                right_repr = "()"
            else:
                if prefix == '':
                    new_prefix = ''
                else:
                    new_prefix = prefix + '1'
                right_repr = self.right.rec_repr(new_prefix)
            res = "(%s %s%s %s)" % (left_repr, prefix, str(self.value), right_repr)
        return res

    @property
    def is_leaf(self):
        return self.left is None and self.right is None

    """The following methods parse a string into a BTree.
    The grammar is the following:
    ROOT := ( INNER
    INNER := ) | VALUE ) | ROOT VALUE ROOT )
    VALUE := [^(^)]+ (any string of characters that aren't a parenthesis) 

    Heavily influenced by these posts:
    * https://stackoverflow.com/questions/19749883/how-to-parse-parenthetical-trees-in-python
    * http://blog.erezsh.com/how-to-write-a-calculator-in-70-python-lines-by-writing-a-recursive-descent-parser/
    """
    @staticmethod
    def tokenize(s):
        """split the input string in suitable tokens."""
        regex = "[^\(^\)]+|\(|\)"
        tokens = re.findall(regex, s.replace(' ', ''))
        return iter(tokens)

    @classmethod
    def parse_root(cls, tokens):
        cur = next(tokens)
        if cur != '(':
            raise ParseError('Expected left paren, got %s instead' % cur)
        return cls.parse_inner(tokens)

    @classmethod
    def parse_inner(cls, tokens):
        cur = next(tokens)
        if cur == ')':
            # case 1: )
            return None
        elif cur != '(':
            # case 2: VALUE )
            result = cls(cur)
        else:
            # case 3: ROOT VALUE ROOT )
            left = cls.parse_inner(tokens)
            value = next(tokens)
            if value in '()':
                raise ParseError('Expected value, got %s instead' % cur)
            right = cls.parse_root(tokens)
            result = cls(value, left, right)
        # make sure that next token is ')' for cases 2 and 3
        cur = next(tokens)
        if cur != ')':
            raise ParseError('Expected right paren, got %s instead' % cur)
        return result

    @classmethod
    def from_string(cls, s):
        return cls.parse_root(cls.tokenize(s))

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
    s = t.rec_repr()
    print(s)
    s2 = repr(BTree(3, BTree(2)))
    print(s2)
    print(BTree.from_string(s))
    print(in_order(t))