import requests
import re
import sys
import time
import os
import argparse
from bs4 import BeautifulSoup
from functools import partial
from multiprocessing import Pool, TimeoutError, cpu_count
from fake_useragent import UserAgent

ua = UserAgent().random

parser = argparse.ArgumentParser(
    description='Argument parser for dork-scanner')
parser.add_argument(
    '-S', '--search', help='String to be searched for', default='1')
parser.add_argument(
    '-E', '--engine', help='Search engine to be used', default='1')
parser.add_argument(
    '-P', '--page', help='Number of pages to search in', default='1')
parser.add_argument('-Pr', '--process',
                    help='Number of parallel processes', default='1')
results = parser.parse_args(sys.argv[1:])


def googleSearch(string, start):
    urls = []
    payload = {'q': string, 'start': start}
    headers = {'User-agent': ua}
    req = requests.get('http://www.google.com/search',
                       payload, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    h3tags = soup.findAll('cite', attrs={'class': 'iUh30'})
    for h3 in h3tags:
        try:
            urls.append(h3.text)
        except:
            continue
    return urls
