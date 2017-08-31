import unittest
from permutations import permutation_product_A, permutation_product_B

class PremutationTest(unittest.TestCase):

    def setUp(self):
        #example from TAoCP
        self.knuth = [(1, 3, 6, 7), (2, 3, 4), (1, 5, 4), (6, 1, 4, 5), (2, 7, 6, 1, 5)]
        self.knuth_res = [(1, 4, 7), (2, 3, 5)]
        self.perm1 = [(1, 2, 3), (4, 6)]
        self.inv_perm1 = [(4, 6), (1, 3, 2)]

    def test_permutation_product_A(self):
        #identity -> nothing happens
        self.assertEqual(permutation_product_A([]), [])
        self.assertEqual(permutation_product_A([(1,)]), [])
        #example from TAoCP
        self.assertEqual(permutation_product_A(self.knuth), self.knuth_res)
        #product with an inverse should yield identity
        self.assertEqual(permutation_product_A(self.perm1 + self.inv_perm1), [])
        self.assertEqual(permutation_product_A([self.perm1, self.inv_perm1]), [])

    def test_permutation_product_B(self):
        #identity -> nothing happens
        self.assertEqual(permutation_product_B([]), [])
        self.assertEqual(permutation_product_B([(1,)]), [])
        #example from TAoCP
        self.assertEqual(permutation_product_B(self.knuth), self.knuth_res)
        #product with an inverse should yield identity
        self.assertEqual(permutation_product_B(self.perm1 + self.inv_perm1), [])
        self.assertEqual(permutation_product_B([self.perm1, self.inv_perm1]), [])