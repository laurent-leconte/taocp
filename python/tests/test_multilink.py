import unittest
from multilink import build_data_table


class MultilinkTest(unittest.TestCase):

    def test_algo_A(self):
        sequence = ((1, 'A'), (3, 'B'), (7, 'C'), (7, 'D'), (3,'E'), (3, 'F'), (4, 'G'), (1, 'H'),
                    (5, 'F'), (8, 'G'), (5, 'B'), (5, 'C'), (9, 'E'), (9, 'D'), (9, 'G'))
        symbols, data = build_data_table(sequence)
        expected_symbols = ['A1', 'B5', 'C5', 'D9', 'E9', 'F5', 'G9', 'H1']
        for symbol in expected_symbols:
            self.assertTrue(symbol in symbols.values())
        names = ['prev', 'parent', 'name', 'child', 'sib']
        expected_data = {
            'A1': [None, None, 'A', 'B3', 'H1'],
            'E3': [None, 'A1', 'E', None, 'F3'],
            'F5': ['F3', 'H1', 'F', 'G8', 'B5'],
            'C5': ['C7', 'H1', 'C', 'E9', None],
            'G9': ['G8', 'C5', 'G', None, None]
        }
        for (k, v) in expected_data.items():
            for (name, value) in zip(names, v):
                self.assertEqual(getattr(data[k], name), value)