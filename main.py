import csv
from dateutil.parser import parse
import argparse


def get_file_name():
    parser = argparse.ArgumentParser()
    parser.add_argument("pathtocsv", help="path to the csv file containing stock information")
    args = parser.parse_args()
    return args.pathtocsv


def main():
    filename = get_file_name()
    print(filename)
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print(f'Name: {row[0]}\t Date: {row[1]}\t Price: {row[2]}.')
                line_count += 1
        print(f'Processed {line_count} lines.')


if __name__ == "__main__":
    main()
