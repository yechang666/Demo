import json
import demjson
'''
    非标准的json，key值不带括号的json文件处理为key带括号json
'''
cc = {'id':1, 'name':'jack', 'status':None}
file_path = "test.json"
with open(file_path,'r', encoding="utf-8") as file_read:
    dd = file_read.read()
    # print(type(dd))
    ff = demjson.decode(dd)
    print(ff)
with open('test1.json', 'w', encoding="utf-8") as file_write:
    json.dump(ff, file_write, ensure_ascii=False)
