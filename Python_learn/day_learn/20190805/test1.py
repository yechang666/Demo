import random
import time
import chardet
import datetime
import json
import requests
import re
# aa = {'a':1, 'b': 2, 'c': 3}
# zz = time.tzname
# for x in zz:
#     print(x)
#     # print(chardet.detect(x))
#     print(x.encode('latin-1').decode('gbk'))

# ss = []
# for i in range(0,123):
#     mm = chr(i)
#     ss.append(mm)
# print(ss)
# url = 'http://fes-dev.silkwave.tv:10080/v1/silkwave/slt'
url = 'http://fes.gvmedia.com.cn/v1/silkwave/slt'
# url = 'http://fessbm.gvmedia.com.cn/v1/silkwave/slt'
result = requests.get(url)
data = result.text
ss = json.loads(data)
# for i in range(30):
cc = []
mm =ss["Service"]
# print(len(mm))
for i in mm:
    if i["serviceCategory"] == 1 or i["serviceCategory"] == 2:
        print(i["shortServiceName"])

