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

engineDict = {
    'google': {
        'payload': {
            'q': 'string',
            'first': 'start'
        },
        'link': 'http://www.google.com/search',
        'tags': {
            'options': 'cite',
            'attr': {
                'class': 'iUh30'
            }
        }
    },

    'bing': {
        'payload': {
            'q': 'string',
            'first': 'start'
        },
        'link': 'https://www.bing.com/search',
        'tags': {
            'options': 'li',
            'attr': 'b_algo'
        }
    },

    'baidu': {
        'payload': {
            'q': 'string',
            'first': 'start'
        },
        'link': 'http://www.baidu.com/s',
        'tags': {
            'options': 'h3',
            'attr': 't'
        }
    },
}


def search(engine, string, start):
    engineSearch = engineDict[engine]
    urls = []
    headers = {'User-agent': ua}
    req = requests.get(engineSearch['link'],
                       engineSearch['payload'], headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    tags = soup.findAll(engineSearch['tags']
                        ['options'], engineSearch['tags']['attr'])

    for tag in tags:
        try:
            if engine == 'google':
                urls.append(tag.text)
            elif engine == 'bing':
                urls.append(tag.find('a').attrs['href'])
            else:
                urlu = tag.find('a').attrs['href']
                link = requests.get(urlu)
                urls.append(link.url)
        except:
            continue
    return urls
