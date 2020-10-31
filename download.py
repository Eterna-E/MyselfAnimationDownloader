import os

link = input("type link:")
fileName = input("type fileName:")

print('link:',link)
print('filename:',fileName)

cmd1='ffmpeg -protocol_whitelist "file,http,https,tcp,tls" '
cmd2='-i "'+link+'" '
cmd3='-c copy ".\\'+str(fileName)+'.mp4"'
os.system(cmd1+cmd2+cmd3)