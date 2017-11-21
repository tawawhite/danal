from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
import json
from .settings import *
from pymongo import MongoClient
import time


def get_jsonparsed_data(url):
    while True:
        try:
            response = urlopen(url)
            data = response.read().decode("utf-8")
            return json.loads(data)
        except HTTPError as e:
            print(e)
            time.sleep(2)
            continue
        except URLError as e:
            print(e)
            time.sleep(2)
            continue


connection = MongoClient()
db = connection.bynet

# db.drop_collection('Serpstat')

f = open('./data/serpstat_domains.txt')
for line in f.readlines():
    domain = line.rstrip('\n')
    url = 'http://api.serpstat.com/v3/domain_info?query=' + domain + '&token=' + token + '&se=g_by'
    data = get_jsonparsed_data(url)
    db.Serpstat.insert(data)
    print(domain)
    time.sleep(1)