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
    """Parses command line arguments to get the csv filepath.
    Throws error if not positional argument supplied.

    Returns:
    string: filepath.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "pathtocsv", help="path to the csv file containing stock information")
    args = parser.parse_args()
    return args.pathtocsv


def date_parser(inputStr):
    """DateTime Factory.

    Parameter:
    inputStr (string): date string.

    Returns:
    DateTime: Datetime object parsed from input string.
    """
    return dateutil_parser(inputStr, dayfirst=True, yearfirst=False)


def get_stock_prices(filename):
    """Parses csv file to get prices of all the stocks.

    Parameter:
    filename (string): csv file path.

    Returns:
    dict: dictionary of stock prices with company code as key and a list of StockPrice tuples.
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


def stock_prices_in_range(prices, start_date, end_date):
    """Filters stock prices of a particular stock to a given date range.

    Parameter:
    prices (list): StockPrice list of a single stock.
    start_date (DateTime): Start date of filter.
    end_date (DateTime): End date of filter.

    Returns:
    list: List of stock prices in the given range.
    """
    return list(price for price in prices if start_date <= price.date <= end_date)


def mean(price_range):
    """Calculates mean of a StockPrices list.
    List must contains at least a single element.
    For empty lists returns 0.

    Parameter:
    price_range (list): StockPrice list of a single stock.

    Returns:
    float: Mean price.
    """
    prices_in_range = list(p.price for p in price_range)
    if not prices_in_range:
        return 0
    return statistics.mean(prices_in_range)


def std(price_range):
    """Calculates standard deviation of a StockPrices sample
    If list contains less than two elements returns 0.

    Parameter:
    price_range (list): StockPrice list of a single stock.

    Returns:
    float: Standard deviation of the supplied price list.
    """
    prices_in_range = list(p.price for p in price_range)

    # variance requires at least two data points
    if len(prices_in_range) < 2:
        return 0
    return statistics.stdev(prices_in_range)


def max_profit(prices):
    """Calculates maximum possible profit for a given range of stock prices
    Expects the data to be sorted in increasing order wrt date.

    Parameter:
    price_range (list): StockPrice list of a single stock.

    Returns:
    tuple: StockPrice of buy and sell date to which will maximize profit.
    """
    length = len(prices)
    if length < 2:
        return None, None

    buy = prices[0]
    sell = prices[1]
    profit = sell.price - buy.price

    for i in range(1, length):
        if prices[i].price - buy.price > profit:
            sell = prices[i]
            profit = sell.price - buy.price

        if prices[i].price < buy.price:
            buy = prices[i]

    if profit == 0:
        return None, None
    return buy, sell


def get_date_range():
    """Prompts user to get start and end date.
    If end date is greater than start date raises ValueError
    """
    start_date = date_parser(input("From which date you want to start? :- "))
    end_date = date_parser(input("Till which date you want to analyze? :- "))

    if start_date > end_date:
        raise ValueError(f"The Start Date ({start_date}) cannot be greater than the End Date {end_date}")

    return start_date, end_date


def parse_queries(prices, start_date, end_date):
    """Prints mean, standard deviation and date range to maximize profit with maximum possible profit.

    Parameter:
    prices (list): StockPrice list of a single stock.
    start_date (DateTime): Start date of filter.
    end_date (DateTime): End date of filter.
    """
    price_range = stock_prices_in_range(prices, start_date, end_date)
    if not price_range:
        print("No data found for the stock in given date range")
        return

    mean_price = mean(price_range)
    std_price = std(price_range)
    buy, sell = max_profit(price_range)
    if buy is None or sell is None:
        print("No profit can not be made in the specified date range")
    else:
        profit = sell.price - buy.price
        print(
            f"Here is your result :- \nMean: {mean_price}\tStd: {std_price}\tBuy Date: {buy.date.strftime('%d-%b-%Y')}\tSell date: {sell.date.strftime('%d-%b-%Y')}\tProfit: {profit}")


def is_done():
    """Prompts for user input if they want to continue or not.
    Possible options for input: y/n.
    """
    while True:
        option = input("Do You Want to Continue? (y or n) :- ").lower()
        if option == "y":
            return False
        if option == "n":
            return True
        print("Sorry I Do Not Understand.")


def get_stock_name(stocks):
    """Prompts user to get stock name they want to query.
    Partial matches are allowed.
    If stock name is not found asks again.
    """
    while True:
        possible_name = input("\nWhich Stock You Need to Process? :- ").upper()
        if possible_name in stocks:
            return possible_name
        name, score = process.extractOne(possible_name, stocks.keys())
        if score < 50:
            print("Stock Name Not Found.")
            continue
        option = input(f"Do You Mean {name}? (y):- ")
        if option.lower() == "y":
            return name.upper()
        print("Please Try Again.")


def main():
    filename = get_file_name()
    try:
        stock_prices = get_stock_prices(filename)
    except IOError as e:
        print("Sorry Error Reading Input File. Cause: ", e)
        exit(1)
    except (ValueError, TypeError) as v:
        print("Error in Input File Parsing. Cause: ", v)
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
            print(f"Error in Parsing Query. Cause: {v}. Please try again.")

        if is_done():
            break

    print("Thanks For Using. Goodbye!")


if __name__ == "__main__":
    main()
