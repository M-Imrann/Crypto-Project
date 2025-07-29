import unittest
from unittest.mock import patch
from api_client import CurrencyAPIClient
from config import CURRENCIES


class TestCurrencyApiClient(unittest.TestCase):
    """
    Test Class to test the fetch data and get historical data functions.
    """
    def setUp(self):
        self.client = CurrencyAPIClient(api_key="test")

    @patch("api_client.requests.get")
    def test_fetch_data_success(self, mock_get):
        """
        Test case to test the fetch data function.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "meta": {"last_updated_at": "2025-07-24T00:00:00Z"},
            "data": {"USD": {"value": 1.0}}
            }

        data = self.client._fetch_data("latest")
        self.assertIn("meta", data)
        self.assertIn("data", data)

    @patch.object(CurrencyAPIClient, "_fetch_data")
    def test_get_historical_data(self, mock_fetch):
        """
        Test case to test the get_historical data function.
        """
        mock_fetch.return_value = {
            "meta": {"last_updated_at": "2025-07-24T00:00:00Z"},
            "data": {currency: {"value": 1.0} for currency in CURRENCIES}
        }
        data = self.client.get_historical_data(2)
        self.assertGreaterEqual(len(data), 1)


if __name__ == '__main__':
    unittest.main()
