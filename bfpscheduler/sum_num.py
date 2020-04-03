# -*- coding: utf-8 -*-
# @Time     :2020/04/02 10:07
# @Author   :lzw
# @Email    :601923086@qq.com
# @File     :sum_num.py
tt = []
# with open("resource/num.txt") as f:
#     cc = f.readline()
#     aa = f.readline()
#     while aa != "":
#         dd = aa
#         aa = f.readline()
#         for i in aa:
#             if i == '0':
#                 tt.append(dd)
#                 break
#             else:
#                 break
# for i in tt:
#     print(i,end='')


def replace_for():
    for m in range(0,500,39):
        for n in range(77,118):
            print("从第%s个CTB开始删除，删除%s个CTB" % (39*13 + m, n))

replace_for()