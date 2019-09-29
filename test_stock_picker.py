import unittest
target = __import__("main")


class TestEmptyRange(unittest.TestCase):
    def setUp(self):
        self. price_range = []

    def test_mean(self):  
        self.assertEqual(target.mean(self.price_range), 0)

    def test_std(self):
        self.assertEqual(target.std(self.price_range), 0)

    def test_max_profit(self):
        self.assertTupleEqual(target.max_profit(self.price_range), (0, 0))


if __name__ == '__main__':
    unittest.main()
