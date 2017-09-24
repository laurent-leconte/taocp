import unittest
from permutations import table_to_cycles, cycles_to_table
from permutations import permutation_product_A, permutation_product_B, permutation_inverse_I
from linkedlists import topological_sort, polynomial_addition, polynomial_multiplication
from trees import BTree, in_order


class PermutationTest(unittest.TestCase):

    def setUp(self):
        #example from TAoCP
        self.knuth = [(1, 3, 6, 7), (2, 3, 4), (1, 5, 4), (6, 1, 4, 5), (2, 7, 6, 1, 5)]
        self.knuth_res = [(1, 4, 7), (2, 3, 5)]
        self.perm1 = [(1, 2, 3), (4, 6)]
        self.perm2 = [(1, 4, 5, 2)]
        self.perm3 = [(1, 4), (2, 7), (3, 5)]
        self.perm1_table = [0, 2, 3, 1, 6, 5, 4]
        self.inv_perm1 = [(1, 3, 2), (4, 6)]

    def test_table_to_cycles(self):
        self.assertEqual(table_to_cycles(list(range(6))), [])
        self.assertEqual(table_to_cycles(self.perm1_table), self.perm1)

    def test_cycles_to_table(self):
        self.assertEqual(cycles_to_table([]), [0,1])
        self.assertEqual(cycles_to_table(self.perm1), self.perm1_table)
        perm2_table = cycles_to_table(self.perm2)
        self.assertEqual(table_to_cycles(perm2_table), self.perm2)

    def test_permutation_product_A(self):
        #identity -> nothing happens
        self.assertEqual(permutation_product_A([]), [])
        self.assertEqual(permutation_product_A([(1,)]), [])
        #example from TAoCP
        self.assertEqual(permutation_product_A(self.knuth), self.knuth_res)
        #product with an inverse should yield identity
        self.assertEqual(permutation_product_A(self.perm1 + self.inv_perm1), [])
        self.assertEqual(permutation_product_A([self.perm1, self.inv_perm1]), [])
        self.assertEqual(permutation_product_A(self.perm3 + self.perm3), [])

    def test_permutation_product_B(self):
        #identity -> nothing happens
        self.assertEqual(permutation_product_B([]), [])
        self.assertEqual(permutation_product_B([(1,)]), [])
        #example from TAoCP
        self.assertEqual(permutation_product_B(self.knuth), self.knuth_res)
        #product with an inverse should yield identity
        self.assertEqual(permutation_product_B(self.perm1 + self.inv_perm1), [])
        self.assertEqual(permutation_product_B([self.perm1, self.inv_perm1]), [])
        self.assertEqual(permutation_product_B(self.perm3 + self.perm3), [])

    def test_permutation_inverse_I(self):
        self.assertEqual(permutation_inverse_I([]),[])
        self.assertEqual(permutation_inverse_I(self.perm1), self.inv_perm1)
        self.assertEqual(permutation_inverse_I(self.perm3), self.perm3)


class LinkedlistsTest(unittest.TestCase):
    def setUp(self):
        self.simple = [(2, 3), (4, 5), (1, 2), (3, 4)]
        self.knuth = [(9, 2), (3, 7), (7, 5), (5, 8), (8, 6), (4, 6), (1, 3), (7, 4), (9, 5), (2, 8)]
        self.knuth_res = [9, 2, 1, 3, 7, 5, 8, 4, 6]
        self.loop = [(1, 2), (2, 3), (3, 1), (1, 4)]
        self.zero = [(0, (0, 0, -1))]
        self.p = [(1, (1, 0, 0)), (1, (0, 1, 0)), (1, (0, 0, 1))] + self.zero
        self.minus_p = [(-1, (1, 0, 0)), (-1, (0, 1, 0)), (-1, (0, 0, 1))] + self.zero
        self.q = [(1, (2, 0, 0)), (-2, (0, 1, 0)), (-1, (0, 0, 1))] + self.zero
        self.p2 = [(1, (2, 0, 0)), (2, (1, 1, 0)), (2, (1, 0, 1)), (1, (0, 2, 0)), (2, (0, 1, 1)), (1, (0, 0, 2))] + self.zero
        self.p_plus_q = [(1, (2, 0, 0)), (1, (1, 0, 0)), (-1, (0, 1, 0))] + self.zero
        self.pq = [(1, (3, 0, 0)), (1, (2, 1, 0)), (1, (2, 0, 1)), (-2, (1, 1, 0)), (-1, (1, 0, 1)), (-2, (0, 2, 0))] +\
                  [(-3, (0, 1, 1)), (-1, (0, 0, 2))] + self.zero
        self.one = [(1, (0, 0, 0))] + self.zero

    def test_topological_sort(self):
        self.assertEqual(topological_sort(self.simple), [1, 2, 3, 4, 5])
        self.assertEqual(topological_sort(self.knuth), self.knuth_res)

    def test_topological_sort_loop(self):
        self.assertRaises(ValueError, topological_sort, self.loop)

    def test_polynomial_addition_zero(self):
        self.assertEqual(polynomial_addition(self.zero, self.zero), self.zero)
        self.assertEqual(polynomial_addition(self.p, self.zero), self.p)
        self.assertEqual(polynomial_addition(self.zero, self.p), self.p)

    def test_polynomial_addition(self):
        self.assertEqual(polynomial_addition(self.p, self.q), self.p_plus_q)
        self.assertEqual(polynomial_addition(self.p, self.minus_p), self.zero)
        self.assertEqual(polynomial_addition(self.p_plus_q, self.minus_p), self.q)

    def test_polynomial_addition_commut(self):
        self.assertEqual(polynomial_addition(self.q, self.p), self.p_plus_q)
        self.assertEqual(polynomial_addition(self.minus_p, self.p), self.zero)

    def test_polynomial_multiplication_zero(self):
        self.assertEqual(polynomial_multiplication(self.zero, self.zero), self.zero)
        self.assertEqual(polynomial_multiplication(self.p, self.zero), self.zero)
        self.assertEqual(polynomial_multiplication(self.zero, self.p), self.zero)

    def test_polynomial_multiplication_one(self):
        self.assertEqual(polynomial_multiplication(self.one, self.one), self.one)
        self.assertEqual(polynomial_multiplication(self.p, self.one), self.p)
        self.assertEqual(polynomial_multiplication(self.one, self.p), self.p)

    def test_polynomial_multiplication(self):
        self.assertEqual(polynomial_multiplication(self.p, self.q), self.pq)
        self.assertEqual(polynomial_multiplication(self.q, self.p), self.pq)
        self.assertEqual(polynomial_multiplication(self.p, self.p), self.p2)

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
