# import urllib3
from urllib import request
from bs4 import BeautifulSoup
import os


def parse_year_page(year_url):
    for m in range(3, 12):
        for d in range(1, 32):
            # print("month_{:02}/day_{:02}".format(m, d))
            parse_path = "/".join([year_url, "month_{:02}/day_{:02}".format(m, d)])
            print("path: {}".format(parse_path))
            html = request.urlopen(parse_path)
            soup = BeautifulSoup(html, 'html.parser')
            for link in (soup.find_all("li")):
                print(link)
            exit(0)

if __name__ == '__main__':
    year_url = "http://gd2.mlb.com/components/game/mlb/year_2018"
    parse_year_page(year_url)
