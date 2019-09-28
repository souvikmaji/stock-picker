import csv
from dateutil.parser import parse
import argparse


def get_file_name():
    parser = argparse.ArgumentParser()
    parser.add_argument("pathtocsv", help="path to the csv file containing stock information")
    args = parser.parse_args()
    return args.pathtocsv


def get_stock_prices(filename, stock_prices):
    with open(filename) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for row in csv_reader:
            date_price = {parse(row["StockDate"]): float(row["StockPrice"])}
            stock_prices.setdefault(row["StockName"], []).append(date_price)


def main():
    filename = get_file_name()

    stock_prices = {}
    get_stock_prices(filename, stock_prices)

    print(stock_prices)


if __name__ == "__main__":
    main()
