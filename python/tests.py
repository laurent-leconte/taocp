import unittest
from permutations import permutation_product

class PremutationTest(unittest.TestCase):

    def setUp(self):
        #example from TAoCP
        self.knuth = [(1, 3, 6, 7), (2, 3, 4), (1, 5, 4), (6, 1, 4, 5), (2, 7, 6, 1, 5)]
        self.knuth_res = [(1, 4, 7), (3, 5, 2)]
        self.perm1 = [(1, 2, 3), (4, 6)]
        self.inv_perm1 = [(4, 6), (2, 1, 3)]

    def test_permutation_product(self):
        #identity -> nothing happens
        self.assertEqual(permutation_product([]), [])
        self.assertEqual(permutation_product([(1,)]), [])
        #example from TAoCP
        self.assertEqual(permutation_product(self.knuth), self.knuth_res)
        #product with an inverse should yield identity
        self.assertEqual(permutation_product(self.perm1 + self.inv_perm1), [])
        self.assertEqual(permutation_product([self.perm1, self.inv_perm1]), [])