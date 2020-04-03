import copy
import json
dd = {
            "id": 1,
            "file_name": "../run/bfp/gaicibi.ts.m3u8"
        }
list1 = []
for i in range(1, 100):
    dd['id'] = i
    list1.append(copy.deepcopy(dd))
str_json = json.dumps(list1,indent=2,ensure_ascii=False)
print(str_json)