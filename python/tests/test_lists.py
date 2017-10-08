import unittest
from linkedlists import topological_sort, polynomial_addition, polynomial_multiplication


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
