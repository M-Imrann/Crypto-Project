import unittest
from unittest.mock import mock_open, patch
from file_writer import FileWriter


class TestFileWriter(unittest.TestCase):
    def setUp(self):
        self.currency_data = {
            "USD": {
                "rates": [1.0, 1.1],
                "roc": [10.0],
                "ma_short": [1.0, 1.05],
                "ma_long": [1.0, 1.05],
                "volatility": 0.05,
                "performance": 10.0,
                "latest_rate": 1.1
            }
        }
        self.dates = ["2025-07-23", "2025-07-24"]

    @patch("builtins.open", new_callable=mock_open)
    def test_write_comprehensive_csv(self, mock_file):
        FileWriter.write_comprehensive_csv(
            self.dates,
            self.currency_data,
            filename="test.csv"
            )
        mock_file.assert_called_with("test.csv", "w", newline='')

    @patch("file_writer.FPDF.output")
    @patch("file_writer.FPDF.add_page")
    @patch("file_writer.FPDF.cell")
    @patch("file_writer.FPDF.set_font")
    def test_generate_pdf(self, mock_output):
        FileWriter.generate_pdf(
            self.currency_data,
            2,
            filename="test.pdf"
            )
        mock_output.assert_called_once()


if __name__ == '__main__':
    unittest.main()
