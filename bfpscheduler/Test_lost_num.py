# -*- coding: utf-8 -*-
# @Time     :2020/03/23 16:46
# @Author   :lzw
# @Email    :601923086@qq.com
# @File     :Test_lost_num.py
import os

import renew_file

B_S = 13
ADT_LEN = 39
DS = 10
PS = 3
CTB_LEN = 1104





def read_File(file, m, n):
    with open(file, 'rb') as f:
        head = f.read(B_S * ADT_LEN * CTB_LEN + m * CTB_LEN)
        write_CTB(head)
        f.read(n * CTB_LEN)
        write_CTB(f.read())
        # read_ctb = random.randint(0,100)
        # first_read_ctb = 21
        # read_ctb = 30
        # count = f.read(CTB_LEN * read_ctb)
        # count = f.read(CTB_LEN * first_read_ctb)
        # print(count)
        # # sum = 0
        # # del_ctb = 0
        # while len(count) > 0:
        #     write_CTB(count)
        #     # del_ctb = random.randint(0, 20)
        #     # del_count = f.read(CTB_LEN * del_ctb)
        #     del_count = f.read(CTB_LEN * 1)
        #     count = f.read()
        #     # count = f.read()
        #     # sum = sum + del_ctb
        #     # sum = sum + 1

    # return (sum- del_ctb) * CTB_LEN
    return n * CTB_LEN

def write_CTB(count):
    write_ctb.write(count)


if __name__ == '__main__':
    for m in range(39,40):
        for n in range(78,79):
            print("从第%s个CTB开始删除，删除%s个CTB" % (39*13 + m, n))
            read_path_data = "D:/ASDT/input/interleav-srcfile-8.data"
            read_path_ts = "D:/ASDT/input/interleav-srcfile-8.ts"
            write_path_ts = "D:/ASDT/out/interleav-srcfile-8.data"
            ts_file_size = os.path.getsize(read_path_ts)
            write_ctb = open(write_path_ts, 'wb')
            del_ctb_size = read_File(read_path_data, m, n)
            print("The file name is:%s,the file size is:%s,the delete rate is :%.2f%%" % (read_path_data, ts_file_size, del_ctb_size / ts_file_size * 100))
            write_ctb.close()
            md5_size_new = renew_file.run_a("interleav-srcfile-8.data", ts_file_size)
            md5_size_old = renew_file.get_file_md5("interleav-srcfile-8.ts")
            print(md5_size_old, md5_size_new)
            if md5_size_old == md5_size_new:
                print("The file name is：%s Restore success" % ("interleav-srcfile-8.data"))
            else:
                print("The file name is：%s Failed" % ("interleav-srcfile-8.data"))
            os.chdir("D:/ASDT/out/")
            # os.remove("interleav-srcfile-8.data")
            # os.remove("interleav-srcfile-8.data.ts")

