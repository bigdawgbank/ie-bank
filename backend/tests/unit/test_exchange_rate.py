import unittest
from unittest.mock import patch, mock_open
from iebank_api.models import ExchangeRate

class TestExchangeRate(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='{"exchange_rate": {"USD_TO_EURO_EXCHANGE_RATE": "0.95"}}')
    def test_get_exchange_rate_usd_to_eur(self, mock_file):
        exchange_rate = ExchangeRate()
        rate = exchange_rate.get_exchange_rate('$', '€')
        self.assertEqual(rate, 0.95)

    @patch('builtins.open', new_callable=mock_open, read_data='{"exchange_rate": {"USD_TO_EURO_EXCHANGE_RATE": "0.95"}}')
    def test_get_exchange_rate_eur_to_usd(self, mock_file):
        exchange_rate = ExchangeRate()
        rate = exchange_rate.get_exchange_rate('€', '$')
        self.assertEqual(rate, round(1 / 0.95, 2))

    @patch('builtins.open', new_callable=mock_open, read_data='{"exchange_rate": {"USD_TO_EURO_EXCHANGE_RATE": "0.95"}}')
    def test_get_exchange_rate_same_currency(self, mock_file):
        exchange_rate = ExchangeRate()
        rate = exchange_rate.get_exchange_rate('$', '$')
        self.assertEqual(rate, 1)

if __name__ == '__main__':
    unittest.main()
