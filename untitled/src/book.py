# coding=utf-8
import requests
from lxml import etree
import time
for i in range(2,115):
    str1 = str(i)
    url = 'https://www.52shuku.me/tuili/1121/hrKe_' + str1 + '.html'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'
    }
    html = requests.get(url, headers=headers)
    html.encoding = html.apparent_encoding
    result = etree.HTML(html.text)
    # print(html.text)
    book_data = result.xpath("/html/body/section/div/div/article/p/text()")
    # book_data.replace(u'\u3000', u' ').replace(u'\xa0', u'')
    text = ''.join(book_data)
    # print(type(text))
    file = open("D:/book.txt",'a')
    file.write(text)
file.close()
print("写入完成")
