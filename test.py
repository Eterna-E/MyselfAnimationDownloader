import requests as rq
from bs4 import BeautifulSoup
import time
import os
import threading
import random

homepageLink='https://myself-bbs.com/thread-45326-1-4.html'
# homepageLink = input("type Link：")
time.sleep(1)

response = rq.get(homepageLink)
html_doc = response.text
soup = BeautifulSoup(html_doc, 'lxml')
AnimeName = BeautifulSoup(str(soup.find_all('div', class_="z")), 'lxml').find_all('a')
for tag in AnimeName:
  if tag.get('href') and ('thread' in tag.get('href')):
    # print(tag)
    AnimeName = str(tag.string)
print(AnimeName)
print('')
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
    print(tag.get('data-href')) # 影片部分連結
    link = tag.get('data-href').replace('https://v.myself-bbs.com/player/play/','https://vpx57.myself-bbs.com/')+'/720p.m3u8'
    videom3u8Link.append(link.replace('\r',''))

print(len(videoTitle))
print(videoTitle)
print(len(videom3u8Link))
print(videom3u8Link)

for i in range(len(videoTitle)):
    print(videoTitle[i])
    print(videom3u8Link[i])
