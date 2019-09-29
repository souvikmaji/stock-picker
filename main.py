import argparse
import csv
import statistics
from collections import namedtuple
from operator import attrgetter

from dateutil.parser import parse as dateutil_parser

from fuzzywuzzy import process
from pyfiglet import Figlet

StockPrice = namedtuple("StockPrice", "date, price")


def get_file_name():
    """Parses command line arguments to get the csv filepath

    Returns: filepath
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "pathtocsv", help="path to the csv file containing stock information")
    args = parser.parse_args()
    return args.pathtocsv


def date_parser(inputStr):
    """DateTime Factory.

    input: date string
    output: DateTime
    """
    return dateutil_parser(inputStr, dayfirst=True, yearfirst=False)


def get_stock_prices(filename):
    """Parses csv file to get prices of all the stocks

    Returns: dictionary of stock prices with company code as key and a list of price variations as values
    """
    stock_prices = {}
    with open(filename) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for row in csv_reader:
            stock_price = StockPrice(date=date_parser(
                row["StockDate"]), price=float(row["StockPrice"]))
            stock_prices.setdefault(
                row["StockName"].upper(), []).append(stock_price)

    # sort list of StockPrices based on date
    for stock, prices in stock_prices.items():
        stock_prices[stock] = sorted(prices, key=attrgetter("date"))

    return stock_prices


def print_stock_prices(stock_prices):
    for stock, prices in stock_prices.items():
        print(stock, prices)


def stock_prices_in_range(prices, start_date, end_date):
    return list(price for price in prices if start_date <= price.date <= end_date)


def mean(price_range):
    prices_in_range = list(p.price for p in price_range)
    if not prices_in_range:
        return 0
    return statistics.mean(prices_in_range)


def std(price_range):
    prices_in_range = list(p.price for p in price_range)
    # variance requires at least two data points
    if len(prices_in_range) < 2:
        return 0
    return statistics.stdev(prices_in_range)


def max_profit(prices):
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


def get_date_range():
    start_date = date_parser(input("From which date you want to start? :- "))
    end_date = date_parser(input("Till which date you want to analyze? :- "))

    if start_date > end_date:
        raise ValueError(f"The Start Date ({start_date}) cannot be greater than the End Date {end_date}")

    return start_date, end_date


def parse_queries(prices, start_date, end_date):
    price_range = stock_prices_in_range(prices, start_date, end_date)
    if not price_range:
        print("No data found for the stock in given date range")
        return

    mean_price = mean(price_range)
    std_price = std(price_range)
    buy, sell = max_profit(price_range)
    if buy is None or sell is None:
        print("")

    profit = sell.price - buy.price

    if profit <= 0:
        print("No profit can not be made in the specified date range")
        return
    print(
        f"Here is your result :- \nMean: {mean_price}\tStd: {std_price}\tBuy Date: {buy.date}\tSell date: {sell.date}\tProfit: {profit}")


def is_done():
    while True:
        option = input("Do you want to continue? (y or n) :- ").lower()
        if option == "y":
            return False
        if option == "n":
            return True
        print("Sorry I do not understand.")


def get_stock_name(stocks):
    while True:
        possible_name = input("\nWhich stock you need to process? :- ").upper()
        if possible_name in stocks:
            return possible_name
        name, score = process.extractOne(possible_name, stocks.keys())
        if score < 50:
            print("Stock name not found.")
            continue
        option = input(f"Do you mean {name}? (y):- ")
        if option.lower() == "y":
            return name.upper()
        print("Please try again.")


def main():
    filename = get_file_name()
    try:
        stock_prices = get_stock_prices(filename)
    except IOError as e:
        print("Sorry Error Reading File. Cause: ", e)
        exit(1)
    except ValueError as v:
        print("Error in file parsing. Cause: ", v)
        exit(1)

    # welcome text
    print(Figlet(font="starwars").renderText("Stock Picker"))
    print("Welcome Agent!")

    while True:
        stock_name = get_stock_name(stock_prices)
        try:
            start, end = get_date_range()
            parse_queries(stock_prices[stock_name], start, end)
        except ValueError as v:
            print(f"Error in parsing query. Cause: {v}. Please try again.")

        if is_done():
            break

    print("Thanks for using. Goodbye!")


if __name__ == "__main__":
    main()
