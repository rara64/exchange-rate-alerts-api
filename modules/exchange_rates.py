import requests

class RateProviderError(Exception): pass
class RateNotFoundError(Exception): pass

def get_current_market_rate(base_currency : str, quote_currency : str) -> float:
    try:
        url = f"https://api.frankfurter.app/latest?amount=1&from={base_currency}&to={quote_currency}"
        response = requests.get(url, timeout=4)
        response.raise_for_status()
        data = response.json()

        rate = data.get("rates", {}).get(quote_currency)       
        if rate is None:
            raise RateNotFoundError()

        return float(rate)

    except requests.RequestException as e:
        raise RateProviderError(str(e))