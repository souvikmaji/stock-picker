import csv
from dateutil.parser import parse as date_parser
import argparse
import statistics
from operator import attrgetter
from collections import namedtuple

StockPrice = namedtuple("StockPrice", "date, price")


def get_file_name():
    parser = argparse.ArgumentParser()
    parser.add_argument("pathtocsv", help="path to the csv file containing stock information")
    args = parser.parse_args()
    return args.pathtocsv


def get_stock_prices(filename):
    stock_prices = {}
    with open(filename) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for row in csv_reader:
            stock_price = StockPrice(date=date_parser(row["StockDate"]), price=float(row["StockPrice"]))
            stock_prices.setdefault(row["StockName"], []).append(stock_price)

    # sort list of StockPrices based on date
    for stock, prices in stock_prices.items():
        stock_prices[stock] = sorted(prices, key=attrgetter('date'))

    return stock_prices


def print_stock_prices(stock_prices):
    for stock, prices in stock_prices.items():
        print(stock, prices)


def stock_prices_in_range(prices, start_date, end_date):
    return list(price for price in prices if start_date <= price.date <= end_date)


def mean(prices, start_date, end_date):
    prices_in_date_range = list(p.price for p in stock_prices_in_range(prices, start_date, end_date))
    if not prices_in_date_range:
        return 0
    return statistics.mean(prices_in_date_range)


def std(prices, start_date, end_date):
    prices_in_date_range = list(p.price for p in stock_prices_in_range(prices, start_date, end_date))
    # variance requires at least two data points
    if len(prices_in_date_range) < 2:
        return 0
    return statistics.stdev(prices_in_date_range)


def max_profit(stock_prices, start_date, end_date):
    prices = stock_prices_in_range(stock_prices, start_date, end_date)
    print(prices)

    length = len(prices)
    if length < 2:
        return 0, 0

    buy = prices[0]
    sell = prices[1]
    max_profit = sell.price - buy.price

    for i in range(1, length):
        if prices[i].price - buy.price > max_profit:
            sell = prices[i]
            max_profit = sell.price - buy.price

        if prices[i].price < buy.price:
            buy = prices[i]

    return buy, sell


def main():
    filename = get_file_name()

    stock_prices = get_stock_prices(filename)
    print_stock_prices(stock_prices)

    stock_name = input("Welcome Agent! Which stock you need to process? :- ").upper()
    if stock_name in stock_prices:
        prices = stock_prices[stock_name]
        start_date = date_parser(input("From which date you want to start? :- "))
        end_date = date_parser(input("Till which date you want to analyze? :- "))
        # max_diff(stock_prices[stock_name])
        if start_date > end_date:
            print("start date is greater than end date")
        else:
            mean_price = mean(prices, start_date, end_date)
            std_price = std(prices, start_date, end_date)
            buy, sell = max_profit(prices, start_date, end_date)
            profit = sell.price - buy.price

            if profit <= 0:
                print("No profit can not be made in the specified date range")
            else:
                print(
                    f"Here is your result :- \nMean: {mean_price}\tStd: {std_price}\tBuy Date: {buy.date}\tSell date: {sell.date}\tProfit: {profit}")
 
    else:
        print("Oops. Stock Not Found")


if __name__ == "__main__":
    main()
