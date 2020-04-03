# coding=utf-8
import requests
from lxml import etree
import time
url2 = '/r/467571688/467571690.htm?ln=152_478334_97698234_1_1_L14L8L51L3&purl=%2Fr%2Fp%2Fcatalog.jsp%3Fbid%3D467571688&page=1&vt=3'
for i in range(20):
    # str1 = str(i)
    url1 = 'http://wap.cmread.com'
    url = url1 + url2
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'
    }
    html = requests.get(url, headers=headers)
    html.encoding = html.apparent_encoding
    result = etree.HTML(html.text)
    # print(html.text)
    book_data = result.xpath("/html/body/section[3]/div[2]//p/text()")
    url2 = result.xpath("//div[@class='charpterBox']//a[3]/@href")
    url2 = str(url2[0])
    text = ''.join(book_data)
    # print(type(text))
    file = open("D:/shidaguobao_kunlongju.txt",'a',encoding='utf-8')
    file.write(text)
file.close()
print("写入完成")
