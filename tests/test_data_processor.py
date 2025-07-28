import unittest
from data_processor import DataProcessor


class TestDataProcessor(unittest.TestCase):
    def test_calculate_volatility(self):
        self.assertAlmostEqual(DataProcessor.calculate_volatility([1, 2, 3]),
                               1.0)

    def test_claculate_performance(self):
        self.assertAlmostEqual(DataProcessor.calculate_performance([1, 2]),
                               100.0)

    def test_calculate_performance_empty(self):
        self.assertAlmostEqual(DataProcessor.calculate_performance([]), 0.0)

    def test_calculate_roc(self):
        roc = DataProcessor.calculate_roc([1, 2, 4])
        self.assertEqual(len(roc), 2)
        self.assertAlmostEqual(roc[0], 100.0)

    def test_calculate_moving_average(self):
        ma = DataProcessor.calculate_moving_average([1, 2, 3, 4], 2)
        self.assertEqual(ma, [1.0, 1.5, 2.5, 3.5])

    def test_process_currency_data(self):
        data = [
            {"meta": {"last_updated_at": "2025-07-24T12:00:00Z"},
             "data": {"USD": {"value": 1.0}, "EUR": {"value": 2.0}}},
            {"meta": {"last_updated_at": "2025-07-23T12:00:00Z"},
             "data": {"USD": {"value": 1.1}, "EUR": {"value": 2.1}}},
        ]
        from config import CURRENCIES
        CURRENCIES.clear()
        CURRENCIES.extend(["USD", "EUR"])
        dates, result = DataProcessor.process_currency_data(data, 2)
        self.assertIn("USD", result)
        self.assertIn("EUR", result)


if __name__ == '__main__':
    unittest.main()
