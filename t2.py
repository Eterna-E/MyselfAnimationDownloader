import requests as rq
from bs4 import BeautifulSoup
import json

link = 'https://v.myself-bbs.com/vpx/45326/009/'

response = rq.get(link)
json_doc = response.text
print(json_doc)

j = json.loads(json_doc)
print(j['video']['720p'])