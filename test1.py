# https://v.myself-bbs.com/vpx/45326/009/

import requests as rq
from bs4 import BeautifulSoup
import subprocess
from multiprocessing import Pool
import time
import multiprocessing
import os
import threading
import json

homepageLink='https://myself-bbs.com/thread-45326-1-4.html'
homepageLink = input("type Link：")
time.sleep(1)

response = rq.get(homepageLink)
html_doc = response.text
soup = BeautifulSoup(html_doc, 'lxml')
# various fancybox.iframe
# 所有的超連結
soup = BeautifulSoup(str(soup.find_all('ul', class_="main_list")[0]), 'lxml')
# print(ul_tag)
a_tags = soup.find_all('a')
videoTitle = []
videom3u8Link = []
for tag in a_tags:
  # 輸出超連結的文字
  if tag.get('href') and ('javascript' in tag.get('href')):
    print(str(tag.string)) # 影片名稱
    videoTitle.append(str(tag.string))
  if tag.get('data-href') and ('v.myself-bbs.com' in tag.get('data-href')):
    link = tag.get('data-href').replace('https://v.myself-bbs.com/player/play/','https://v.myself-bbs.com/vpx/')
    temp = rq.get(link)
    json_doc = temp.text
    j = json.loads(json_doc)
    link = 'https://vpx57.myself-bbs.com/'+j['video']['720p']
    print(link)
    videom3u8Link.append(link)

time.sleep(1)

# print(len(videoTitle))
# print(videoTitle)
# print(len(videom3u8Link))
# print(videom3u8Link)

# for i in range(len(videoTitle)):
#     print(videoTitle[i])
#     print(videom3u8Link[i])