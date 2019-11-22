# import urllib3
from urllib import request
from bs4 import BeautifulSoup
import os
import urllib.parse
import requests


def download_inning_data(gid_url, out_path):
    inning_url = os.path.join(gid_url, "inning/inning_all.xml")
    # urllib.parse.urljoinだと、末尾からファイル名と判定すると（/で終わっていない場合）、ファイル名を除外して結合してしまうので、、
    print(inning_url)
    response = requests.get(inning_url)
    with open(out_path, 'wb') as file:
        file.write(response.content)

def parse_year_page(year_url, out_dir):
    for m in range(7, 8):
        for d in range(21, 32):
            # print("month_{:02}/day_{:02}".format(m, d))
            parse_path = "/".join([year_url, "month_{:02}/day_{:02}".format(m, d)])
            print("path: {}".format(parse_path))
            html = request.urlopen(parse_path)
            soup = BeautifulSoup(html, 'html.parser')
            link_string_list = [link.string.strip() for link in (soup.find_all("li"))]
            for link in link_string_list:
                if link.startswith("gid"):
                    gid_url = os.path.join(parse_path, link)
                    gid = link.replace("/", "")
                    out_path = os.path.join(out_dir, gid+".xml")
                    download_inning_data(gid_url, out_path)
        exit(0)

if __name__ == '__main__':
    year_url = "http://gd2.mlb.com/components/game/mlb/year_2018"
    out_dir = "data"
    parse_year_page(year_url, out_dir)
