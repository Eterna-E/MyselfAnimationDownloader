import requests as rq
from bs4 import BeautifulSoup
import time
import os
import threading
import json
import random
import re

homepageLink='https://myself-bbs.com/thread-45326-1-4.html'
homepageLink = input("type Link：")
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
    link = tag.get('data-href').replace('https://v.myself-bbs.com/player/play/','https://v.myself-bbs.com/vpx/')
    temp = rq.get(link)
    json_doc = temp.text
    j = json.loads(json_doc)
    link = 'https://vpx57.myself-bbs.com/'+j['video']['720p']
    print(link)
    videom3u8Link.append(link)

time.sleep(1)

print(len(videoTitle))
print(videoTitle)
print(len(videom3u8Link))
print(videom3u8Link)

for i in range(len(videoTitle)):
    videoTitle[i] = videoTitle[i].replace('!','！')
    videoTitle[i] = videoTitle[i].replace(':','：')
    # videoTitle[i] = re.sub('[’!"#$%&\'()*+,-./:;<=>?@，?★、…【】《》？“”‘’[\\]^_`{|}~\s]+', "", videoTitle[i])
    print(videoTitle[i])
    print(videom3u8Link[i])

# m3u8 domain name:https://vpx57.myself-bbs.com/45158/001/720p.m3u8
# replace https://v.myself-bbs.com/player/play/45158/012

time.sleep(1)

def run(arg1,arg2) :
    print(arg1,arg2)
    cmd = "ffmpeg -protocol_whitelist \"file,http,https,tcp,tls\" "+'-i "'+arg1+'" '+'-c copy ".\\'+str(arg2)+'.mp4"'
    # subprocess.call(cmd,  shell=True)
    os.system(cmd)

threads = []
startTime = time.time()

for i in range(len(videoTitle)):     # 建立與啟動執行緒
    t = threading.Thread(target = run,
                        args=(videom3u8Link[i], videoTitle[i]))
    t.start()
    threads.append(t)
    time.sleep(0.5+float(format(random.uniform(0,0.5), '.5f')))
    # video_download(url, listbox)

for thread in threads:
    thread.join()

print('動漫名：'+AnimeName)
print('')

fileNotFoundNum = []
fileFounded = 0
fileSize = 0
for i in range(len(videoTitle)):
    # 檢查檔案是否存在
    if os.path.isfile('.\\'+videoTitle[i]+'.mp4'):
        print(videoTitle[i]+'.mp4'+"的檔案存在。大小："+str(os.path.getsize('.\\'+videoTitle[i]+'.mp4'))+' bytes')
        fileFounded+=1
        fileSize+=os.path.getsize('.\\'+videoTitle[i]+'.mp4')
    else:
        print(videoTitle[i]+'.mp4'+"的檔案不存在。")
        fileNotFoundNum.append(i)
if fileNotFoundNum:
    threads = []
    for i in fileNotFoundNum:     # 建立與啟動執行緒
        t = threading.Thread(target = run,
                            args=(videom3u8Link[i], videoTitle[i]))
        t.start()
        threads.append(t)
        time.sleep(0.5)
        # video_download(url, listbox)
    for thread in threads:
        thread.join()

endTime = time.time()
print('----------------------------------------------------')
print('已下載'+str(fileFounded)+'個影片檔案，總共 '+str( format(fileSize/1024/1024, '.2f') )+' MB')
print("總下載時間：", format(endTime - startTime, '.2f') ,'秒，大約 '+ str(format(float(format(endTime - startTime, '.2f'))/60, '.2f')))

# format(random.uniform(0,0.5), '.5f')