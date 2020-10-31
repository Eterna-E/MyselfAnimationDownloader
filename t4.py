# https://vpx15.myself-bbs.com/45326/001/720p.m3u8

# import requests
# url = "https://vpx15.myself-bbs.com/45326/001/720p.m3u8"
# r = requests.get(url)
# print(type(r.status_code))
# with open("test.m3u8", "wb") as code:
# 	code.write(r.content)



# import os

# print(os.system("dir"))
# import datetime
# print( datetime.datetime.now().strftime('%Y%m%d_%H%M%S.%f'))
# import shutil
# shutil.rmtree(".\\download")

from fake_useragent import UserAgent
ua = UserAgent()

print(ua.ie)
print(ua.chrome)
print(ua.random)
print(ua.random)