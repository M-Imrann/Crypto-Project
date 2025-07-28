import unittest
from unittest.mock import patch, MagicMock
import main


class TestMain(unittest.TestCase):
    @patch("main.get_args")
    @patch("main.CurrencyAPIClient")
    @patch("main.DataProcessor")
    @patch("main.FileWriter")
    def test_main_success(self, mock_processor, mock_client, mock_args):
        mock_args.retturn_value = MagicMock(days=2)
        mock_client.return_value.get_historical_data.return_value = [
            {
                "meta": {"last_updated_at": "2025-07-24T12:00:00Z"},
                "data": {"USD": {"value": 1.0}}
            }
        ]
        mock_processor.process_currency_data.return_value = (
            ["2025-07-24", "2025-07-23"],
            {"USD": {
                "rates": [1.0, 1.1],
                "roc": [10.0],
                "ma_short": [1.0, 1.05],
                "ma_long": [1.0, 1.05],
                "volatility": 0.05,
                "performance": 10.0,
                "latest_rate": 1.1
            }}
        )
        with patch("builtins.print"):
            main.main()

    @patch("main.get_args")
    @patch("main.CurrencyAPIClient")
    def test_main_no_data(self, mock_client, mock_args):
        mock_args.return_value = MagicMock(days=2)
        mock_client.return_value.get_historical_data.return_value = []
        with patch("builtins.print"):
            main.main()


if __name__ == '__main__':
    unittest.main()
