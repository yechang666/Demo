# -*- coding: utf-8 -*-
# @Time     :2020/03/17 17:14
# @Author   :lzw
# @Email    :601923086@qq.com
# @File     :Read_CTB.py
import hashlib
import random

import os
import logging
import renew_file

B_S = 13
ADT_LEN = 39
DS = 10
PS = 3
CTB_LEN = 1104

def read_File(file):
    # with open('resource/interleav-srcfile-1.data', 'rb') as f:
    with open(file, 'rb') as f:
        head = f.read(B_S * ADT_LEN * CTB_LEN)
        write_CTB(head)
        # read_ctb = random.randint(0,100)
        first_read_ctb = 10
        read_ctb = 30
        # count = f.read(CTB_LEN * read_ctb)
        count = f.read(CTB_LEN * first_read_ctb)
        print(count)
        sum = 0
        del_ctb = 0
        while len(count) > 0:
            write_CTB(count)
            # del_ctb = random.randint(0, 20)
            # del_count = f.read(CTB_LEN * del_ctb)
            del_count = f.read(CTB_LEN * 4)
            count = f.read(CTB_LEN * read_ctb)
            # count = f.read()
            # sum = sum + del_ctb
            sum = sum + 4

    # return (sum- del_ctb) * CTB_LEN
    return (sum- 4) * CTB_LEN

def write_CTB(count):
    write_ctb.write(count)


if __name__ == '__main__':
    path = "D:/ASDT/input"
    dirs = os.listdir(path)
    # print(dirs)
    data_file_name = []
    ts_file_name = []
    for file in dirs:
        if "data" in file:
            data_file_name.append(file)
        else:
            ts_file_name.append(file)

    for file in data_file_name:
        file1 = "D:/ASDT/input/"
        file2 = "D:/ASDT/out/"
        file1 = file1 + file
        file2 = file2 + file
        file_size = os.path.getsize(file1)
        ts_file = os.path.splitext(file)[0] + ".ts"
        ts_file_size = os.path.getsize("D:/ASDT/input/" + ts_file)
        # print("The file name is:%s,the file size is:%d" % (file,file_size))
        write_ctb = open(file2, 'wb')
        del_ctb_size = read_File(file1)
        print("The file name is:%s,the file size is:%s,the delete rate is :%.2f%%" % (file, file_size,del_ctb_size/file_size*100 ))
        write_ctb.close()
        md5_size_new = renew_file.run_a(file, ts_file_size)

        md5_size_old = renew_file.get_file_md5(ts_file)
        print(md5_size_old, md5_size_new)
        if md5_size_old == md5_size_new:
            print("The file name is：%s Restore success" % (file))
        else:
            print("The file name is：%s Failed" % (file))




