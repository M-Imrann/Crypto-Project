from arg_parser import parse_args
from api_client import CurrencyAPIClient
from data_processor import DataProcessor
from file_writer import FileWriter


def main():
    args = parse_args()
    days = args.days

    # Initialize API client and fetch data
    client = CurrencyAPIClient()
    print(f"Fetching {days} days of currency data...")
    historical_data = client.get_historical_data(days)

    if not historical_data:
        print("Error: No data retrieved. Exiting.")
        return

    print("Processing currency data...")
    dates, currency_data = DataProcessor.process_currency_data(
        historical_data,
        days
        )

    if not currency_data:
        print("Error: Processed data is empty. Exiting.")
        return

    # Get the actual number of days we have data for
    actual_days = min(days, len(dates))

    # Generate outputs
    print("Generating output files...")
    FileWriter.write_comprehensive_csv(dates, currency_data)
    FileWriter.generate_pdf(currency_data, actual_days)

    print("\nProcessing completed successfully!")
    print(f"Processed {actual_days} days of data for"
          f"{len(currency_data)} currencies")
    print("Comprehensive CSV: currency_data.csv")
    print("PDF report: currency_report.pdf")


if __name__ == "__main__":
    main()
