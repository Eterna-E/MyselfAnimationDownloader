import requests as rq
from bs4 import BeautifulSoup
import time
import os
import threading
import json
import random
import re
import requests
import datetime
# from Crypto.Cipher import AES
import shutil
import subprocess
from fake_useragent import UserAgent
from queue import Queue

ua = UserAgent()
# user_agent = ua.random
homepageLink='https://myself-bbs.com/thread-45326-1-4.html'
homepageLink = input("type Link：")
time.sleep(1)

startTime = time.time()

response = rq.get(homepageLink, headers={ 'user-agent': ua.random })
while True:
    if response.status_code == 200:
        print("ok")
        break
    else:
        print("not yet")
        response = rq.get(homepageLink, headers={ 'user-agent': ua.random })
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
    temp = rq.get(link, headers={ 'user-agent': ua.random })
    while True:
        if temp.status_code == 200:
            print("ok")
            break
        else:
            print("not yet")
            temp = rq.get(link, headers={ 'user-agent': ua.random })
    json_doc = temp.text
    j = json.loads(json_doc)
    link = 'https://vpx57.myself-bbs.com/'+j['video']['720p']
    print(link)
    videom3u8Link.append(link)

time.sleep(0.1)
analysis_time = str(format(time.time() - startTime, '.2f'))

print(len(videoTitle))
print(videoTitle)
print(len(videom3u8Link))
print(videom3u8Link)

for i in range(len(videoTitle)):
    videoTitle[i] = videoTitle[i].replace('!','！')
    videoTitle[i] = videoTitle[i].replace(':','：')
    videoTitle[i] = videoTitle[i].replace('?','？')
    # videoTitle[i] = re.sub('[’!"#$%&\'()*+,-./:;<=>?@，?★、…【】《》？“”‘’[\\]^_`{|}~\s]+', "", videoTitle[i])
    print(videoTitle[i])
    print(videom3u8Link[i])

# m3u8 domain name:https://vpx57.myself-bbs.com/45158/001/720p.m3u8
# replace https://v.myself-bbs.com/player/play/45158/012

time.sleep(1)

#-------------------------------------------------------------------
#此處舊的實作方式
# def run(arg1,arg2) :
#     print(arg1,arg2)
#     cmd = "ffmpeg -protocol_whitelist \"file,http,https,tcp,tls\" "+'-i "'+arg1+'" '+'-c copy ".\\'+str(arg2)+'.mp4"'
#     # subprocess.call(cmd,  shell=True)
#     os.system(cmd)

# threads = []
# startTime = time.time()

# for i in range(len(videoTitle)):     # 建立與啟動執行緒
#     t = threading.Thread(target = run,
#                         args=(videom3u8Link[i], videoTitle[i]))
#     t.start()
#     threads.append(t)
#     time.sleep(0.5+float(format(random.uniform(0,0.5), '.5f')))
#     # video_download(url, listbox)

# for thread in threads:
#     thread.join()

#-------------------------------------------------------------------

#-------------------------------------------------------------------
#此處新的實作方式
class Worker(threading.Thread):
  def __init__(self, videom3u8Link, videoTitle, num, semaphore, queue):
    threading.Thread.__init__(self)
    self.num = num
    self.semaphore = semaphore
    self.videom3u8Link = videom3u8Link
    self.videoTitle = videoTitle
    self.queue = queue

  def run(self):
    # 取得旗標
    self.semaphore.acquire()
    print("Semaphore acquired by Worker %d" % self.num)

    # 僅允許有限個執行緒同時進的工作
    print(self.videom3u8Link, self.videoTitle)
    #-------------------------------------------------------------------
    #此處舊的實作方式
    # cmd = "ffmpeg -protocol_whitelist \"file,http,https,tcp,tls\" "+'-i "'+self.videom3u8Link+'" '+'-c copy ".\\'+str(self.videoTitle)+'.mp4"'

    # os.system(cmd)
    #-------------------------------------------------------------------
    ThreadStartTime = time.time()
    #-------------------------------------------------------------------
    #此處新的實作方式
    self.download(self.videom3u8Link)
    #-------------------------------------------------------------------
    time.sleep(1)
    ThreadEndTime = time.time()
    ThreadExecuteTime = ThreadEndTime - ThreadStartTime
    self.queue.put(ThreadExecuteTime)
    # 釋放旗標
    print("Semaphore released by Worker %d" % self.num)
    self.semaphore.release()

  def download(self, url):
    # user_agent = ua.random
    downloaded_file = []
    download_path = os.getcwd() + "\\download"
    if not os.path.exists(download_path):
        os.mkdir(download_path)

    #新建日期文件夹
    download_path = os.path.join(download_path, datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    # XXXX XX XX_XX XX XX_XXXXXX 年月日 時分秒 微秒
    #print download_path
    if not os.path.exists(download_path):
        os.mkdir(download_path)

    # r = requests.get(url)
    # with open(download_path+"\\720p.m3u8", "wb") as f:
    #     f.write(r.content)
    #     f.flush()

    all_content = requests.get(url, headers={ 'user-agent': ua.random })  # 获取第一层M3U8文件内容
    while True:
        if all_content.status_code == 200:
            all_content = all_content.text
            print("ok")
            break
        else:
            print("not yet")
            all_content = requests.get(url, headers={ 'user-agent': ua.random })
    if "#EXTM3U" not in all_content:
        raise BaseException("非M3U8的链接")

    if "EXT-X-STREAM-INF" in all_content:  # 第一层
        file_line = all_content.split("\n")
        for line in file_line:
            if '.m3u8' in line:
                url = url.rsplit("/", 1)[0] + "/" + line # 拼出第二层m3u8的URL
                all_content = requests.get(url, headers={ 'user-agent': ua.random })
                while True:
                    if all_content.status_code == 200:
                        all_content = all_content.text
                        print("ok")
                        break
                    else:
                        print("not yet")
                        all_content = requests.get(url, headers={ 'user-agent': ua.random })

    file_line = all_content.split("\n")
    # print(file_line)

    unknow = True
    key = ""
    for index, line in enumerate(file_line): # 第二层
        if "#EXT-X-KEY" in line:  # 找解密Key
            method_pos = line.find("METHOD")
            comma_pos = line.find(",")
            method = line[method_pos:comma_pos].split('=')[1]
            print("Decode Method：", method)

            uri_pos = line.find("URI")
            quotation_mark_pos = line.rfind('"')
            key_path = line[uri_pos:quotation_mark_pos].split('"')[1]

            key_url = url.rsplit("/", 1)[0] + "/" + key_path # 拼出key解密密钥URL
            res = requests.get(key_url, headers={ 'user-agent': ua.random })
            key = res.content
            print("key：" , key)

        if "EXTINF" in line: # 找ts地址并下载
            unknow = False
            pd_url = url.rsplit("/", 1)[0] + "/" + file_line[index + 1] # 拼出ts片段的URL
            #print pd_url

            res = requests.get(pd_url, headers={ 'user-agent': ua.random })
            while True:
                if res.status_code == 200:
                    print("ok")
                    print(self.videoTitle+"的片段")
                    break
                else:
                    print("not yet")
                    res = requests.get(pd_url, headers={ 'user-agent': ua.random })
            c_fule_name = file_line[index + 1].rsplit("/", 1)[-1]

            # if len(key): # AES 解密
            #     cryptor = AES.new(key, AES.MODE_CBC, key)
            #     with open(os.path.join(download_path, c_fule_name + ".mp4"), 'ab') as f:
            #         f.write(cryptor.decrypt(res.content))
            # else:
            with open(os.path.join(download_path, c_fule_name), 'ab') as f:
                f.write(res.content)
                f.flush()
                print(f.name)
                downloaded_file.append(f.name)
    if unknow:
        raise BaseException("未找到对应的下载链接")
    else:
        print ("下载完成")
    self.merge_file(download_path, downloaded_file)

  def merge_file(self, path, downloaded_file):
    d=downloaded_file
    # print(d)
    with open(path+"\\list.txt", "a") as fp:
        for i in d:
            fp.write("file '"+i+"'\n")
            fp.flush()
    time.sleep(1)
    print(path)
    cmd = "ffmpeg -y -f concat -safe 0 -i \""+path+"\\list.txt\" -c copy \""+self.videoTitle+".mp4\""
    ret = subprocess.check_call(cmd)
    # os.system("ffmpeg -f concat -safe 0 -i \""+path+"\\list.txt\" -c copy \""+self.videoTitle+".mp4\"")
    # os.system("ffmpeg -i \""+path+"\\720p.m3u8\" -c copy \""+self.videoTitle+".mp4\"")
    while 1:
        if os.path.isfile(self.videoTitle+'.mp4') and ret == 0:
            time.sleep(1)
            shutil.rmtree(path)
            break

# 建立旗標
semaphore = threading.Semaphore(8)

threads = []
# startTime = time.time()
q =Queue()

for i in range(len(videoTitle)):     # 建立與啟動執行緒
    t = Worker(videom3u8Link[i], videoTitle[i], i ,semaphore, q)
    time.sleep(0.5)
    t.start()
    threads.append(t)
    # time.sleep(0.5+float(format(random.uniform(0,0.5), '.5f')))
    # time.sleep(1)

for thread in threads:
    thread.join()
#-------------------------------------------------------------------

if os.path.exists(".\\download"):
    shutil.rmtree(".\\download")

time.sleep(1)

VideoDownloadTime = []
for i in range(len(videoTitle)):
    VideoDownloadTime.append(q.get())
    # print(format(q.get(),'.2f'))
# print(VideoDownloadTime)

print('動漫名：'+AnimeName)
print('檢查檔案是否遺漏')

fileNotFoundNum = []
fileFounded = 0
fileSize = 0
for i in range(len(videoTitle)):
    # 檢查檔案是否存在
    if os.path.isfile('.\\'+videoTitle[i]+'.mp4'):
        # print(videoTitle[i]+'.mp4'+"的檔案存在。大小："+str(os.path.getsize('.\\'+videoTitle[i]+'.mp4'))+' bytes')
        print(videoTitle[i]+'.mp4'+"的檔案存在。大小："+str(format(os.path.getsize('.\\'+videoTitle[i]+'.mp4')/1024/1024, '.2f'))+' MB，下載時間：'+str(format(VideoDownloadTime[i],'.2f'))+'秒')
        fileFounded+=1
        fileSize+=os.path.getsize('.\\'+videoTitle[i]+'.mp4')
    else:
        print(videoTitle[i]+'.mp4'+"的檔案不存在。")
        fileNotFoundNum.append(i)
if fileNotFoundNum:
    threads = []
    for i in fileNotFoundNum:     # 建立與啟動執行緒
        # t = threading.Thread(target = run,
        #                     args=(videom3u8Link[i], videoTitle[i]))
        t = Worker(videom3u8Link[i], videoTitle[i], i ,semaphore,q)
        t.start()
        threads.append(t)
        time.sleep(0.5)
        # video_download(url, listbox)
    for thread in threads:
        thread.join()

endTime = time.time()
print('----------------------------------------------------')
print('已下載'+str(fileFounded)+'個影片檔案，總共 '+str( format(fileSize/1024/1024, '.2f') )+' MB')
print("總下載時間：", format(endTime - startTime, '.2f') ,'秒，大約 '+ str(format(float(format(endTime - startTime, '.2f'))/60, '.2f'))+'分鐘')
print('影片連結分析時間大約：'+analysis_time+"秒，影片檔案下載時間大約："+format(float(format(endTime - startTime, '.2f'))-float(analysis_time), '.2f')+"秒")
input("按任意鍵退出")
# format(random.uniform(0,0.5), '.5f')