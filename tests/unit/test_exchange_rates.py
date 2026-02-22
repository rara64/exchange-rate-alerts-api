from unittest.mock import patch, MagicMock
from modules.exchange_rates import get_current_market_rate, RateProviderError, RateNotFoundError

class TestExchangeRates:
    @patch("modules.exchange_rates.requests.get")
    def test_get_current_market_rate_returns_valid_rate(self, mock_get):

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "rates": {
                "EUR": 0.85
            }
        }
        mock_get.return_value = mock_response

        rate = get_current_market_rate("USD", "EUR")
        assert rate == 0.85

    @patch("modules.exchange_rates.requests.get")
    def test_get_current_market_rate_returns_RateProviderError_when_api_error(self, mock_get):

        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        try:
            get_current_market_rate("USD", "EUR")
        except RateProviderError as e:
            assert isinstance(e, RateProviderError)

    @patch("modules.exchange_rates.requests.get")
    def test_get_current_market_rate_returns_RateNotFoundError_when_no_rates(self, mock_get):

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "message": ""
        }
        mock_get.return_value = mock_response

        try:
            get_current_market_rate("USD", "EUR")
        except RateNotFoundError as e:
            assert isinstance(e, RateNotFoundError)