import csv
import random


def main():
    rows = list(get_rows())
    rand = random.randint(0, len(rows)-1)
    header = rows[rand]['header']
    content = rows[rand]['content']
    url = rows[rand]['url']
    print(header, url)
    print(rows[4]['content'])


def get_rows():
    f = open('output.csv', 'r', encoding='utf-8')

    reader = csv.DictReader(f)
    return reader
