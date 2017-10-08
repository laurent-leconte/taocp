import unittest
from trees import BTree, in_order


class TreesTest(unittest.TestCase):
    def setUp(self):
        l = BTree("B", BTree("D"))
        f = BTree("F", BTree("H"), BTree("J"))
        r = BTree("C", BTree("E", None, BTree("G")), f)
        self.tree = BTree("A", l, r)

    def test_in_order(self):
        self.assertEqual(in_order(None), [])
        self.assertEqual(in_order(BTree("A", BTree("B"), BTree("C"))), ["B", "A", "C"])
        self.assertEqual(in_order(self.tree), ['D', 'B', 'A', 'E', 'G', 'C', 'H', 'F', 'J'])
