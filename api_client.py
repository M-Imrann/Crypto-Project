import requests
from datetime import datetime, timedelta
from config import API_KEY, CURRENCIES, BASE_URL


class CurrencyAPIClient:
    def __init__(self, api_key=API_KEY):
        self.api_key = api_key
        self.cache = {}

    def _fetch_data(self, endpoint, date=None):
        cache_key = f"{endpoint}-{date}" if date else endpoint
        if cache_key in self.cache:
            return self.cache[cache_key]

        params = {'apikey': self.api_key}
        url = BASE_URL + endpoint

        if date:
            params['date'] = date
        params['currencies'] = ",".join(CURRENCIES)

        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            self.cache[cache_key] = data
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {cache_key}: {e}")
            return None

    def get_historical_data(self, days):
        collected_data = []
        distinct_dates = set()
        current_date = datetime.now() - timedelta(days=1)

        # Get today's data
        today_data = self._fetch_data("latest")
        if today_data and today_data.get('data'):
            actual_date = today_data['meta']['last_updated_at'][:10]
            distinct_dates.add(actual_date)
            collected_data.append(today_data)
            days -= 1

        # Get historical data
        while days > 0:
            date_str = current_date.strftime('%Y-%m-%d')
            if date_str in distinct_dates:
                current_date -= timedelta(days=1)
                continue

            data = self._fetch_data("historical", date_str)
            if data and data.get('data'):
                actual_date = data['meta']['last_updated_at'][:10]
                if actual_date not in distinct_dates:
                    distinct_dates.add(actual_date)
                    collected_data.append(data)
                    days -= 1

                    # Ensure all currencies are present
                    for currency in CURRENCIES:
                        if currency not in data['data']:
                            print(f"Warning: {currency}"
                                  f"missing on {actual_date}")
            current_date -= timedelta(days=1)

            if current_date < datetime.now() - timedelta(days=365):
                print("Reached 1-year limit, stopping collection")
                break

        return collected_data
