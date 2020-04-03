# -*- coding: utf-8 -*-
# @Time     :2020/03/19 15:51
# @Author   :lzw
# @Email    :601923086@qq.com
# @File     :renew_file.py
import hashlib
import os
import subprocess
def run_a(file, file_size):
    os.chdir("D:\\ASDT\\out")
    os.rename(file,"outfile.data")
    dd = os.system('a.exe > log.txt')
    file3 = file
    file = file + ".ts"
    os.rename('out.bin',file)
    os.rename("outfile.data",file3)
    with open(file, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read(file_size))
        _hash = md5obj.hexdigest()
    return str(_hash).upper()

def get_file_md5(file_path):
    """
    获取文件md5值
    :param file_path: 文件路径名
    :return: 文件md5值
    """
    os.chdir("D:\\ASDT\\input")
    with open(file_path, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        _hash = md5obj.hexdigest()
    return str(_hash).upper()

