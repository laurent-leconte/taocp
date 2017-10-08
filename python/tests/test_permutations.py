import unittest
from permutations import table_to_cycles, cycles_to_table
from permutations import permutation_product_A, permutation_product_B, permutation_inverse_I


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
