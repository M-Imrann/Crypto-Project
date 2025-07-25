import os
import csv
from fpdf import FPDF


class FileWriter:
    @staticmethod
    def write_comprehensive_csv(dates,
                                currency_data,
                                filename="output/currency_data.csv"
                                ):
        os.makedirs("output", exist_ok=True)
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            # Comprehensive headers with all metrics
            headers = [
                'Date', 'Currency',
                'Rate',
                'Daily ROC (%)',
                '7-Day MA',
                '30-Day MA',
                'Volatility',
                'Performance (%)',
                'Latest Rate',
                'Latest Daily ROC (%)'
            ]
            writer.writerow(headers)

            for i, date in enumerate(dates):
                for currency, data in currency_data.items():
                    if i >= len(data['rates']):
                        continue

                    # Daily metrics
                    rate = data['rates'][i]

                    # Daily ROC calculation
                    daily_roc = ''
                    if i > 0 and i-1 < len(data['roc']):
                        daily_roc = data['roc'][i-1]

                    # Moving averages
                    ma7 = data['ma_short'][i] if i < len(data['ma_short']) else ''
                    ma30 = data['ma_long'][i] if i < len(data['ma_long']) else ''

                    # Summary metrics
                    volatility = data['volatility']
                    performance = data['performance']
                    latest_rate = data['latest_rate']
                    latest_roc = data['roc'][-1] if data['roc'] else 0.0

                    writer.writerow([
                        date,
                        currency,
                        round(rate, 6),
                        round(daily_roc, 4) if isinstance(daily_roc, float) else daily_roc,
                        round(ma7, 6) if isinstance(ma7, float) else ma7,
                        round(ma30, 6) if isinstance(ma30, float) else ma30,
                        round(volatility, 6),
                        round(performance, 4),
                        round(latest_rate, 6),
                        round(latest_roc, 4)
                    ])

    @staticmethod
    def generate_pdf(currency_data, days, filename="output/currency_report.pdf"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, f"Currency Analysis Report ({days} Days)", 0, 1, 'C')

        # Performance ranking
        sorted_currencies = sorted(
            currency_data.items(),
            key=lambda x: x[1]['performance'],
            reverse=True
        )
        top_3 = sorted_currencies[:3]
        bottom_3 = sorted_currencies[-3:]

        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, f"Performance Ranking ({days}-day period)", 0, 1)

        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "Top 3 Performers:", 0, 1)
        for currency, data in top_3:
            pdf.cell(0, 10, f"{currency}: {data['performance']:.2f}%", 0, 1)

        pdf.cell(0, 10, "Bottom 3 Performers:", 0, 1)
        for currency, data in bottom_3:
            pdf.cell(0, 10, f"{currency}: {data['performance']:.2f}%", 0, 1)

        # Volatility and latest ROC
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Currency Metrics", 0, 1)

        headers = ["Currency", "Volatility", "Latest Rate",
                   f"{days}-Day Perf. (%)", "Latest Daily ROC (%)"]
        col_widths = [40, 40, 40, 50, 50]

        pdf.set_font("Arial", 'B', 12)
        for i, header in enumerate(headers):
            pdf.cell(col_widths[i], 10, header, 1)
        pdf.ln()

        pdf.set_font("Arial", '', 12)
        for currency, data in currency_data.items():
            latest_roc = data['roc'][-1] if data['roc'] else 0.0
            pdf.cell(col_widths[0], 10, currency, 1)
            pdf.cell(col_widths[1], 10, f"{data['volatility']:.6f}", 1)
            pdf.cell(col_widths[2], 10, f"{data['latest_rate']:.4f}", 1)
            pdf.cell(col_widths[3], 10, f"{data['performance']:.2f}%", 1)
            pdf.cell(col_widths[4], 10, f"{latest_roc:.4f}%", 1)
            pdf.ln()

        pdf.output(filename)
