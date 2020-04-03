#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2018/10/20 10:32
# @Author  : deli Guo
# @Site   :
# @File   : test3.py
# @Software  : PyCharm
import pymysql
import pandas as pd
# 定义链接到mysql的函数，返回连接对象
# db_name是当前数据库的名字
import time


def getcon(db_name):
    # host是选择连接哪的数据库localhost是本地数据库，port是端口号默认3306
    #user是使用的人的身份，root是管理员身份，passwd是密码。db是数据库的名称，charset是编码格式
    conn=pymysql.connect(host="localhost",port=3306,user='root',passwd='123456',db=db_name,charset='utf8')
    # 创建游标对象
    cursor1=conn.cursor()
    return conn,cursor1
# 定义读取文件并且导入数据库数据sql语句
def insertData(db_name,table_name):
    # 调用链接到mysql的函数，返回我们的conn和cursor1
    conn,cursor1=getcon(db_name)
    # 使用pandas 读取csv文件
    df=pd.read_csv('C:/Users/Administrator/Desktop/message.csv',nrows=1000)
    #使用for循环遍历df，是利用df.values，但是每条数据都是一个列表
    # 使用counts计数一下，方便查看一共添加了多少条数据
    start = time.time()
    counts = 0
    # for each in df.values:
    #     # 每一条数据都应该单独添加，所以每次添加的时候都要重置一遍sql语句
    #     sql = 'insert into '+table_name+'(name1,name2,name3,name4,name5,name6,name7,name8,name9,name10)'+' values('
    #     # 因为每条数据都是一个列表，所以使用for循环遍历一下依次添加
    #     for i,n in enumerate(each):
    #     # for i, n in range(10):
    #         # 这个时候需要注意的是前面的数据可以直接前后加引号，最后加逗号，但是最后一条的时候不能添加逗号。
    #         # 所以使用if判断一下
    #         if i < (len(each) - 1):
    #             #因为其中几条数据为数值型，所以不用添加双引号
    #             if i==2:
    #                 sql = sql + '"' + str(n) + '"' + ','
    #             else:
    #                 sql = sql + str(n) + ','
    #         else:
    #             sql = sql + str(n)
    #     sql = sql + ');'
    #     # print(sql)
    #     # 当添加当前一条数据sql语句完成以后，需要执行并且提交一次
    #     cursor1.execute(sql)
    #     # 提交sql语句执行操作
    #     conn.commit()
    #     # 没提交一次就计数一次
    #     counts+=1
    #     #使用一个输出来提示一下当前存到第几条了
    #     # print('成功添加了'+str(counts)+'条数据 ')
    for stu in df.values:
        stu = (tuple(stu))
        sql = "insert INTO ocean (name1,name2,name3,name4,name5,name6,name7,name8,name9,name10) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
        cursor1.execute(sql % stu)
        conn.commit()
    end = time.time()
    print(end-start)
    return conn,cursor1,counts
# 主函数
def main(db_name,table_name):
    conn, cursor1,counts =insertData(db_name,table_name)
    # 当添加完成之后需要关闭我们的游标，以及与mysql的连接
    print(counts)
    cursor1.close()
    conn.close()
# 判断一下，防止再次在其他文件调用当前函数的时候会使用错误，多次调用
if __name__=='__main__':
    main('mysql','ocean')
