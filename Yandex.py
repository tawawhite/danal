from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from .settings import *
from pymongo import MongoClient
import time
import xml.etree.ElementTree as ET


def get_limit_ynadex():
    hour = int(time.strftime("%H"))
    if (hour > 7) and (hour < 20):
        return 1
    else:
        return 2


def get_jsonparsed_data(url):
    while True:
        try:
            response = urlopen(url)
            data = response.read().decode("utf-8")
            tree = ET.fromstring(data)
            count = 0
            for neighbor in tree.iter('found-docs'):
                count = neighbor.text
                break
            return count
        except HTTPError as e:
            print(e)
            return False
        except URLError as e:
            print(e)
            time.sleep(2)
            continue


connection = MongoClient()
db = connection.bynet

f = open('./data/yanndex_domains.txt')
for line in f.readlines():
    domain = line.rstrip('\n')
    url = "https://yandex.ru/search/xml?user=" + Yandex_user + "&key=" + Yandex_key + "&query=site%3A" + domain + "&lr=149&l10n=ru&sortby=tm.order%3Dascending&filter=strict&groupby=attr%3D%22%22.mode%3Dflat.groups-on-page%3D10.docs-in-group%3D1"
    data = get_jsonparsed_data(url)
    if data:
        db.Yandex.insert({'domain': domain, 'found-docs': data})
    print(domain)
    time.sleep(get_limit_ynadex())
