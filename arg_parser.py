import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description='Fetch and Analyze Currency Data'
        )

    parser.add_argument(
        '--days',
        type=int,
        required=True,
        help='Number of days of historical data to fetch'
        )

    return parser.parse_args()
