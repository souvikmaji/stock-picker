import unittest

target = __import__("main")

sp = target.StockPrice


class TestEmptyRange(unittest.TestCase):
    def setUp(self):
        self.price_range = []

    def test_mean(self):
        self.assertEqual(target.mean(self.price_range), 0)

    def test_std(self):
        self.assertEqual(target.std(self.price_range), 0)


class TestRangeData(unittest.TestCase):
    def setUp(self):
        self.price_range = [sp(0, 1), sp(0, 2), sp(0, 90), sp(0, 10), sp(0, 110)]

    def test_mean(self):
        self.assertEqual(target.mean(self.price_range), 42.6)

    def test_std(self):
        self.assertAlmostEqual(target.std(self.price_range), 52.988678035973, places=5)


class TestMaxProfit(unittest.TestCase):
    def setUp(self):
        self.test_cases = [{"input": [sp(0, 1), sp(0, 2), sp(0, 90), sp(0, 10), sp(0, 110)],
                            "output": (sp(0, 1), sp(0, 110))},
                           {"input": [sp(0, 100), sp(0, 180), sp(0, 260), sp(0, 310), sp(0, 40), sp(0, 535), sp(0, 695)],
                            "output": (sp(0, 40), sp(0, 695))},
                           {"input": [sp(0, 80), sp(0, 2), sp(0, 6), sp(0, 3), sp(0, 100)],
                            "output": (sp(0, 2), sp(0, 100))},
                           {"input": [],
                            "output": (None, None)},
                           {"input": [sp(0, 100)],
                            "output": (None, None)},
                           {"input": [sp(0, 100), sp(0, 100), sp(0, 100)],
                            "output": (None, None)}]

    def test_data(self):
        for test_case in self.test_cases:
            self.assertTupleEqual(target.max_profit(
                test_case["input"]), test_case["output"])


if __name__ == '__main__':
    unittest.main()
