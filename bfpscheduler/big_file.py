import json
import copy
dd ={
	"status": 2,
	"end": "2019-11-02T24:00:00+08:00",
	"file_type": 0,
	"file_name": "gaicibi.ts.m3u8",
	"create": "2017-06-04T09:00:00+08:00",
	"start": "2019-01-02T12:00:00+08:00",
	"md5_hex_string": "00-11-22-33-44-55-66-77-88-99-AA-BB-CC-DD-EE-FF",
	"fid": 1,
	"carousel_info": [{
		"duration": 21600,
		"start": "2020-01-06T17:00:00+08:00",
		"repetition_times": 1
	}],
	"rx_type": "",
	"raptor": "1160413118-1046-1084"
}

# dd = {
#
#         "status": 2,
#         "end": "2019-11-02T24:00:00+08:00",
#         "file_type": 0,
#         "file_name": "jyds.ts.m3u8",
#         "create": "2017-06-04T09:00:00+08:00",
#         "start": "2019-01-02T12:00:00+08:00",
#         "md5_hex_string": "00-11-22-33-44-55-66-77-88-99-AA-BB-CC-DD-EE-FF",
#         "fid": 1,
#         "carousel_info": [{
#             "duration": 7200,
#             "start": "2019-11-21T10:00:00+08:00",
#             "repetition_times": 1,
#             "repetition_period": 172800
#         }],
#         "rx_type": "",
#         "raptor": "24333536-22-1084"
#
# }
start_date_year = 2020
start_date_month = 1
start_date_day = 19
start_time_hours = 11
diff_time = 6 #每个文件推送时间
month = [31,28,31,30,31,30,31,31,30,31,30,31] #十二个月
# dd = json.load(dd)
list1 =[]
for i in range(1,50):
    dd['fid']= i
    start_time_hours = start_time_hours + diff_time
    if start_time_hours >= 24:
        start_date_day = start_date_day + 1
        start_time_hours = start_time_hours % 24
    if start_date_day > month[start_date_month - 1]:
        start_date_month = start_date_month + 1
        start_date_day = 1
    if start_time_hours < 10 and start_date_day < 10:
        start = str(start_date_year) + '-' + str(start_date_month) + '-' + '0' + str(start_date_day) + "T" + '0' + str(
            start_time_hours) + ":00:00+08:00"
    elif start_time_hours < 10 and start_date_day >= 10:
        start = str(start_date_year) + '-' + str(start_date_month) + '-' + str(start_date_day) + "T" + '0' + str(
            start_time_hours) + ":00:00+08:00"
    elif start_time_hours >= 10 and start_date_day < 10:
        start = str(start_date_year) + '-' + str(start_date_month) + '-' + '0' + str(start_date_day) + "T" + str(
            start_time_hours) + ":00:00+08:00"
    else:
        start = str(start_date_year) + '-' + str(start_date_month) + '-' + str(start_date_day) + "T" + str(
            start_time_hours) + ":00:00+08:00"
    # print(start)
    dd['carousel_info'][0]['start'] = start
    # list1.append(copy.deepcopy(dd))
    list1.append(copy.deepcopy(dd))

str_json = json.dumps(list1,indent=2,ensure_ascii=False)
print(str_json)