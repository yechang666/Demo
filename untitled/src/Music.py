import requests
from lxml import etree
import time
import jsoup

url = 'https://music.163.com/discover/toplist'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'
}

html = requests.get(url,headers = headers)
# result = html.text
# print(html.status_code)
result = etree.HTML(html.text)
# print(html.text)
song_list = result.xpath("//ul[@class='f-hide']/li/a/text()")
song_data = result.xpath("//*[@id='song-list-pre-data']/text()")
song_data = eval(song_data)
m1 = song_data[0]
for i in range(len(m1)):
    j = len(m1[i]['artists'])
    if(j==1):
        print("曲名:", m1[i]['album']['name'], "歌手:", m1[i]['artists'][0]['name'])
    else:
        print("曲名:", m1[i]['album']['name'], "歌手:", m1[i]['artists'][0]['name'],"/",m1[i]['artists'][1]['name'])





# json_str = json.dumps(song_data[0])
# # print(json_str)
# data1 = json.loads(song_data[0])
# print(data1)
# print(song_data[0]['album']['name'],['artists']['name'])