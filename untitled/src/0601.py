#encoding:utf-8
import csv
import time
# import pymysql.cursors
import mysql.connector
#连接数据库
config={'host':'127.0.0.1',#默认127.0.0.1
        'user':'root',
        'password':'123456',
        'port':3306 ,#默认即为3306
        'database':'mysql',
        'charset':'utf8'#默认即为utf8
        }
# cnn = pymysql.conne
#获取游标
cnn=mysql.connector.connect(**config);
# print("连接成功");
cour=cnn.cursor();

#插入数据

# sql = "select * from information";
# sql = "Insert into information (name,sex,age,height) VALUES ('%s','%s','%s','%s')"
# data = ('黎明',18,'女');
# cour.execute(sql % data);
# for row in cour.fetchall():
#    print(row)
# print(cour)

# cnn.commit()
# print(cursor.rowcount)

#csv读取
sql = "Insert into ocean  VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
csv_file = csv.reader(open('C:/Users/Administrator/Desktop/message.csv','r',encoding='utf-8'))
# # print(csv_file)
# print(type(csv_file))
# start = time.time()
for stu in csv_file:
    # print(stu)
    data = tuple(stu)
    # print(data)
    cour.execute(sql % data)
    cnn.commit()
cnn.close()
print("写入完成")

