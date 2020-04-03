start_date_year = 2019
start_date_month = 11
start_date_day = 26
start_time_hours = 11
diff_time = 6
month = [31,28,31,30,31,30,31,31,30,31,30,31]
for i in range(1, 100):
    # print(i)
    start_time_hours = start_time_hours +  diff_time
    if start_time_hours >= 24:
        start_date_day = start_date_day + 1
        start_time_hours = start_time_hours % 24
    if start_date_day > month[start_date_month-1]:
        start_date_month = start_date_month + 1
        start_date_day = 1
    if start_time_hours < 10 and start_date_day < 10 :
        start = str(start_date_year) + '-' + str(start_date_month) + '-' + '0' + str(start_date_day) + "T" + '0' + str(start_time_hours) + ":00:00+08:00"
    elif start_time_hours < 10 and start_date_day >= 10:
        start = str(start_date_year) + '-' + str(start_date_month) + '-' +str(start_date_day) + "T" + '0' + str(start_time_hours) + ":00:00+08:00"
    elif start_time_hours >= 10 and start_date_day < 10:
        start = str(start_date_year) + '-' + str(start_date_month) + '-' + '0' + str(start_date_day) + "T" + str(start_time_hours) + ":00:00+08:00"
    else:
        start = str(start_date_year) + '-' +  str(start_date_month) + '-' + str(start_date_day) + "T" + str(start_time_hours) + ":00:00+08:00"
    print(start)

