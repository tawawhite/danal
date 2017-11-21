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
            return False
        except URLError as e:
            print(e)
            time.sleep(2)
            continue


connection = MongoClient()
db = connection.bynet

f = open('./data/domains.txt')
for line in f.readlines():
    domain = line.rstrip('\n')
    url = "https://www.googleapis.com/pagespeedonline/v2/runPagespeed?url=http://" + domain + "&strategy=mobile&key=" + API_KEY
    data = get_jsonparsed_data(url)
    if data:
        db.PageSpeedInsights.insert(data)
        print(domain)
    time.sleep(1)
