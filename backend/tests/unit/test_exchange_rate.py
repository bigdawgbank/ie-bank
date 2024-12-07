import unittest
from unittest.mock import patch
from iebank_api.models import ExchangeRate

class TestExchangeRate(unittest.TestCase):

    @patch('iebank_api.models.os.getenv')
    def test_get_exchange_rate_usd_to_eur(self, mock_getenv):
        mock_getenv.return_value = '0.95'  # Mock the exchange rate from USD to EUR
        exchange_rate = ExchangeRate()
        rate = exchange_rate.get_exchange_rate('USD', 'EUR')
        self.assertEqual(rate, 0.95)

    @patch('iebank_api.models.os.getenv')
    def test_get_exchange_rate_eur_to_usd(self, mock_getenv):
        mock_getenv.return_value = '1.06'  # Mock the exchange rate from EUR to USD
        exchange_rate = ExchangeRate()
        rate = exchange_rate.get_exchange_rate('EUR', 'USD')
        self.assertEqual(rate, 1.06)

    @patch('iebank_api.models.os.getenv')
    def test_get_exchange_rate_same_currency(self, mock_getenv):
        exchange_rate = ExchangeRate()
        rate = exchange_rate.get_exchange_rate('USD', 'USD')
        self.assertEqual(rate, 1)

if __name__ == '__main__':
    unittest.main()
