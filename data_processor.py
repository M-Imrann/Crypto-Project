import math
from config import CURRENCIES


class DataProcessor:
    @staticmethod
    def calculate_volatility(rates):
        """
        This will calculate the volatility of each currency.

        Args:
        rates: rates of the currencies

        return: Return the volatility(standard deviation)
        """
        n = len(rates)
        if n < 2:
            return 0.0
        mean = sum(rates) / n
        variance = sum((x - mean) ** 2 for x in rates) / (n - 1)
        return math.sqrt(variance)

    @staticmethod
    def calculate_performance(rates):
        """
        This will calculate the performance of currencies.

        Args:
        rates: rates of the currencies

        return: Return the performance
        """
        if not rates or rates[0] == 0:
            return 0.0
        return ((rates[-1] - rates[0]) / rates[0]) * 100.0

    @staticmethod
    def calculate_roc(rates):
        """
        This will calculate the rate of change of each currency.

        Args:
        rates: rates of the currencies

        return: Return the list of rate of change
        """
        roc = []
        for i in range(1, len(rates)):
            if rates[i-1] != 0:
                change = ((rates[i] - rates[i-1]) / rates[i-1]) * 100.0
                roc.append(change)
            else:
                roc.append(0.0)
        return roc

    @staticmethod
    def calculate_moving_average(rates, window):
        """
        This will calculate the moving average of each currency.

        Args:
        rates: rates of the currencies
        window: no. of days for finding moving average

        return: Return the list of moving average
        """
        ma = []
        for i in range(len(rates)):
            start = max(0, i - window + 1)
            window_rates = rates[start:i+1]
            if window_rates:
                ma.append(sum(window_rates) / len(window_rates))
            else:
                ma.append(rates[i])
        return ma

    @staticmethod
    def process_currency_data(data, days):
        """
        This will process the currency data.

        Args:
        data: A dictionary of currency rates
        days: Number of days of which data is available

        return: It will return dates and calculated results. 
        """
        dates = sorted({d['meta']['last_updated_at'][:10] for d in data})
        currencies = {c: [] for c in CURRENCIES}

        for date in dates:
            for d in data:
                if d['meta']['last_updated_at'].startswith(date):
                    for currency in CURRENCIES:
                        if currency in d['data']:
                            currencies[currency].append(
                                d['data'][currency]['value'])
                        else:
                            # Add 0 for missing currencies
                            currencies[currency].append(0)
                    break

        results = {}
        for currency, rates in currencies.items():
            # Filter out placeholder zeros
            clean_rates = [r for r in rates if r != 0]
            has_data = len(clean_rates) >= 2

            if has_data:
                actual_days = min(len(clean_rates), days)
                recent_rates = clean_rates[-actual_days:]

                roc = DataProcessor.calculate_roc(recent_rates)
                ma_short = DataProcessor.calculate_moving_average(
                    recent_rates, 7)
                ma_long = DataProcessor.calculate_moving_average(
                    recent_rates, 30)

                results[currency] = {
                    'rates': recent_rates,
                    'volatility': DataProcessor.calculate_volatility(
                        recent_rates),
                    'performance': DataProcessor.calculate_performance(
                        recent_rates),
                    'latest_rate': recent_rates[-1],
                    'roc': roc,
                    'ma_short': ma_short,
                    'ma_long': ma_long
                }
            else:
                # Create placeholder data for currencies with insufficient data
                results[currency] = {
                    'rates': rates,
                    'volatility': 0.0,
                    'performance': 0.0,
                    'latest_rate': rates[-1] if rates else 0,
                    'roc': [],
                    'ma_short': rates,
                    'ma_long': rates
                }
                print(f"Warning: Insufficient data for {currency}")

        return dates, results
