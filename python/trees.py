"""Implementation of some of the tree / binary tree algorithms, with added helper methods to build trees from strings.

"""

import re


class ParseError(Exception):
    pass

class MathError(Exception):
    pass

class BTree(object):
    """Simple binary tree class.

    Some shortcomings:
    * No check that children are actually binary tree.
    * Needs a formal definition and management of empty trees.
    * Parsing from string has not been tested robustly.
    * Clunky `rec_repr` function.

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
    """Inorder traversal of a binary tree without recursion (algorithm T from 2.3.1)

    :param t: a `BTree` to traverse
    :return: the list of nodes in inorder
    """
    # step T1 : initialize stack and result list
    res = []
    p = t
    a = []
    # initial pass of step T2/T3
    while p is not None:
        a.append(p)
        p = p.left
    # step T4/T5 : empty stack, occasionally filling it back from right subtrees
    while len(a) > 0:
        p = a.pop()
        res.append(p.value)
        p = p.right
        # step T2/T3 for right subtrees
        while p is not None:
            a.append(p)
            p = p.left
    return res

def differentiate(t, x):
    """Differentiate a tree `t` with respect to variable `x`.

     The algorithm is based on algorithm D from 2.3.2. The main difference is the use of the original tree structure
     (although in `BTree` format) rather than the binary tree transformation. Accordingly, the tree is traversed in
     post- rather than inorder; this is done recursively rather than using a threaded representation.

    :param t: `BTree` to be differentiated. Node structure should be `TYPE|VALUE` where `TYPE` is one of the following:
    `CONST`, `VAR`, `OP`. See tAoCP for the list of supported operators (which also includes a few functions).
    :param x: The variable used for differentiation. If y != x, `VAR|<y>` is considered as a constant.
    :return: `BTree` of the derivative
    """

    # helper functions
    def is_zero(t):
        return t.value == 'CONST|0'

    def is_one(t):
        return t.value == 'CONST|1'

    def zero():
        return BTree('CONST|0')

    def mult(u, v):
        if is_zero(u) or is_zero(v):
            return zero()
        if is_one(u):
            return v
        elif is_one(v):
            return u
        else:
            return BTree('OP|*', u, v)

    def add(u, v):
        if is_zero(u):
            return v
        elif is_zero(v):
            return u
        else:
            return BTree('OP|+', u, v)

    def sub(u, v):
        if is_zero(v):
            return du
        elif is_zero(u):
            return BTree('OP|neg', v)
        else:
            return BTree('OP|-', u, v)

    def div(u, v):
        if is_zero(u):
            return zero()
        elif is_one(v):
            return u
        elif is_zero(v):
            raise MathError("Division by zero")
        else:
            return BTree('OP|/', u, v)

    def pow(u, v):
        if is_zero(u):
            return zero()
        elif is_zero(v) or is_one(u):
            return BTree('CONST|1')
        else:
            return BTree('OP|^', u, v)

    # get type and value of node
    (ty, val) = t.value.split('|')
    # check for leave cases : CONST, VAR
    if ty == 'CONST':
        return zero()
    if ty == 'VAR':
        if val == x:
            return BTree('CONST|1')
        else:
            return zero()

    #at this point `ty` should only be `OP`
    if ty != 'OP':
        raise ParseError("Unexpected type %s" % ty)
    # switch according to operator value. Start with unary operators, using the derivative of the left subtree
    u = t.left
    du = differentiate(u, x)
    du_equals_zero = is_zero(du)
    if val == 'neg':
        if du_equals_zero:
            return zero()
        else:
            return BTree('OP|neg', du)
    elif val == 'ln':
        if du_equals_zero:
            # we're taking ln of a constant, so the derivative should be zero (rather than a math error)
            return zero()
        else:
            return BTree('OP|/', du, u)
    # moving on to binary operators; now we also need the right subtree
    v = t.right
    dv = differentiate(v, x)
    dv_equals_zero = is_zero(dv)
    if val == '+':
        return add(du, dv)
    if val == '-':
        return sub(du, dv)
    if val == '*':
        return add(mult(u, dv), mult(du, v))
    if val == '/':
        left = div(du, v)
        num = mult(u, dv)
        denom = pow(v, BTree('CONST|2'))
        right = div(num, denom)
        return sub(left, right)
    if val == '^':
        # first = D(u) * v * u^(v - 1)
        first = mult(du, mult(v, pow(u, sub(v, BTree('CONST|1')))))
        # second = ln(u) * dv * u^v
        second = mult(BTree('OP|ln', u), mult(dv, pow(u, v)))
        return add(first, second)

if __name__ == '__main__':
    # TODO : turn into real unit tests
    l = BTree('OP|+', BTree('CONST|1'), BTree('VAR|x'))
    r = BTree('OP|-', BTree('VAR|x'), BTree('VAR|y'))
    t = BTree('OP|*', l, r)
    s = t.rec_repr()
    print(s)
    print(differentiate(l, 'x'))
    print(differentiate(r, 'x'))
    d = differentiate(t, 'y')
    print(d)