# from enum import Enum
#
# class VIP(Enum):
#     Yellow = 1
#     Green = 2
#     Black = 3
#
# print(VIP.Yellow.name)
# print(VIP['Yellow'])
# import re
# a = 'C#PythonC#'
# # 处理函数：对sub的第一参数C#进行处理，value即C#
# def convert(value):
#     print(value)
#     matched = value.group()
#     print(matched)
#     return '|' + matched + '|'
#
#
#
# r = re.sub('C#', convert, a)
# print(r)
# import re
# a = 'C#PythonC#'
#
# # 处理函数：对sub的第一参数C#进行处理，value即C#
#
# def convert(value):
#     print(value)
#     matched = value.group()
#     return '|'+matched+'|'
#
#
# r=re.sub('C#',convert,a)
# print(r)
# import re
# a = '8C3721D86'
#
# r1 = re.match('\d', a)
# print(r1)
#
# r2 = re.search('\d', a)
# print(r2)
#
# r3 = re.findall('\D', a)
# print(r3)
#
#
# m = lambda x, y, z: x * x + y + z
# # print(m([i for i in range(10)],[i for i in range(10)],[i for i in range(10)]))
# m1 = [i for i in range(10)]
# m2 = [i for i in range(10)]
# m3 = [i for i in range(10)]
# # print(m(1,2,3))
# s1 = map(m, m1, m2, m3)
# s2 = map(m, m1, m2)
# print(list(s1))
# from functools import reduce
# list_1 = ['1','2','3','4','5']
# r1 = reduce(lambda x, y: x + y, list_1, 'hello')
# print(r1)
def sunday():
    print('俺是星期天')

def monday():
    print('俺是星期一')

def tuesday():
    print('俺是星期二')

def default():
    print('俺是default')

switcher = {  # 注意：()如果直接写在键值中，会导致所有函数都执行
    0: sunday,
    1: monday,
    2: tuesday
}

day = 0

day_name = switcher.get(day,default)()

