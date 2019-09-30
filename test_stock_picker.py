import datetime
import unittest

target = __import__("main")

sp = target.StockPrice


class TestMean(unittest.TestCase):
    def setUp(self):
        self.test_cases = [{"input": [sp(0, 1), sp(0, 2), sp(0, 90), sp(0, 10), sp(0, 110)],
                            "output": 42.6},
                           {"input": [sp(0, 5)],
                            "output": 5},
                           {"input": [],
                            "output": 0}]

    def test_data(self):
        for test_case in self.test_cases:
            self.assertEqual(target.mean(
                test_case["input"]), test_case["output"])


class TestStd(unittest.TestCase):
    def setUp(self):
        self.test_cases = [{"input": [sp(0, 1), sp(0, 2), sp(0, 90), sp(0, 10), sp(0, 110)],
                            "output": 52.988678035973},
                           {"input": [sp(0, 5)],
                            "output": 0},
                           {"input": [sp(0, 5), sp(0, 10)],
                            "output": 3.535533906},
                           {"input": [],
                            "output": 0}]

    def test_std(self):
        for test_case in self.test_cases:
            self.assertAlmostEqual(target.std(
                test_case["input"]), test_case["output"], places=5)


class TestStockPricesInRange(unittest.TestCase):
    def setUp(self):
        self.test_cases = [{"input": [sp(datetime.date(2019, 4, 1), 0), sp(datetime.date(2019, 4, 2), 0), sp(datetime.date(2019, 4, 3), 0), sp(datetime.date(2019, 4, 4), 0), sp(datetime.date(2019, 4, 5), 0)],
                            "start_date": datetime.date(2019, 4, 2),
                            "end_date": datetime.date(2019, 4, 4),
                            "output": [sp(datetime.date(2019, 4, 2), 0), sp(datetime.date(2019, 4, 3), 0), sp(datetime.date(2019, 4, 4), 0)]},
                           {"input": [sp(datetime.date(2019, 4, 1), 0), sp(datetime.date(2019, 4, 2), 0), sp(datetime.date(2019, 4, 3), 0), sp(datetime.date(2019, 4, 2), 0), sp(datetime.date(2019, 4, 1), 0)],
                            "start_date": datetime.date(2019, 4, 2),
                            "end_date": datetime.date(2019, 4, 4),
                            "output": [sp(datetime.date(2019, 4, 2), 0), sp(datetime.date(2019, 4, 3), 0), sp(datetime.date(2019, 4, 2), 0)]},
                           {"input": [sp(datetime.date(2019, 4, 1), 0), sp(datetime.date(2019, 4, 2), 0)],
                            "start_date": datetime.date(2019, 4, 2),
                            "end_date": datetime.date(2019, 4, 2),
                            "output": [sp(datetime.date(2019, 4, 2), 0)]},
                           {"input": [],
                            "start_date": datetime.date(2019, 4, 2),
                            "end_date": datetime.date(2019, 4, 2),
                            "output": []},
                           ]

    def test_data(self):
        for test_case in self.test_cases:
            self.assertListEqual(target.stock_prices_in_range(
                test_case["input"], test_case["start_date"], test_case["end_date"]), test_case["output"])


class TestMaxProfit(unittest.TestCase):
    def setUp(self):
        self.test_cases = [{"input": [sp(0, 1), sp(0, 2), sp(0, 90), sp(0, 10), sp(0, 110)],
                            "output": (sp(0, 1), sp(0, 110))},
                           {"input": [sp(0, 100), sp(0, 180), sp(0, 260), sp(0, 310), sp(0, 40), sp(0, 535), sp(0, 695)],
                            "output": (sp(0, 40), sp(0, 695))},
                           {"input": [sp(0, 80), sp(0, 2), sp(0, 6), sp(0, 3), sp(0, 100)],
                            "output": (sp(0, 2), sp(0, 100))},
                           {"input": [sp(0, 29.321), sp(0, 39.453), sp(0, 28.453), sp(0, 30.453), sp(0, 31.453), sp(0, 35)],
                            "output": (sp(0, 29.321), sp(0, 39.453))},
                           {"input": [sp(0, 29.321),  sp(0, 35.453), sp(0, 28.453), sp(0, 30.453), sp(0, 31.453)],
                            "output": (sp(0, 29.321), sp(0, 35.453))},
                           {"input": [sp(0, 29), sp(0, 31.453), sp(0, 29.321), sp(0, 39.453), sp(0, 28.453), sp(0, 30.453), sp(0, 31.453), sp(0, 35)],
                            "output": (sp(0, 29), sp(0, 39.453))},
                           {"input": [sp(0, 110), sp(0, 100)],
                            "output": (None, None)},
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
