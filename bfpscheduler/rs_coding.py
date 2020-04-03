# @Time     :2019/12/10 10:34
# @Author   :lzw
# @Email    :601923086@qq.com
# @File     :rs_coding.py

# aa = bytearray(b'AB')
# for i in aa:
#     print(i)
# binary_code = ''.join(format(x, '08b') for x in aa)
# print(len(binary_code), binary_code)
# bytes_msg = bytes(int(binary_code[i:i+8], 2) for i in range(0, len(binary_code),8))
# array_msg = bytearray(bytes_msg)
# print(array_msg)
import random

# from reedsolo import RSCodec
# ecc = RSCodec(6)
# byte_msg = ecc.encode('Bingo007')
# print(byte_msg)
# binary_code = ''.join(format(x, '08b') for x in byte_msg)
# print(len(binary_code), binary_code)
# print(binary_code)
# binary_code = list(binary_code)
# binary_code[0*8+2]=str(1-int(binary_code[0*8+2]))
# binary_code[1*8+4]=str(1-int(binary_code[1*8+4]))
# binary_code[3*8+5]=str(1-int(binary_code[3*8+5]))
# binary_code=''.join(binary_code)
# print(binary_code)
# byte_msg = bytes(int(binary_code[i:i+8],2) for i in range(0, len(binary_code),8))
# array_msg = bytearray(byte_msg)
# data = ecc.decode(array_msg)
# # msg = data.decode()
# print(data)
import hashlib
m = hashlib.md5()
m.update(b"123456")
# m.update(b" the spammish repetition")
cc = m.digest()
print(cc.hex())
print(m.hexdigest())
print(cc)
print(type(cc))
# a = 'aabbccddeeff'
# a_bytes = bytes.fromhex(a)
# print(a_bytes)
# aa = a_bytes.hex()
# print(aa)


# gf_exp = [1] * 512
# gf_log = [0] * 256
# x = 1
# for i in range(1, 255):
#     x <<= 1
#     if x & 0x100:
#         x ^= 0x11d
#     gf_exp[i] = x
#     gf_log[x] = i
# for i in range(255, 512):
#     gf_exp[i] = gf_exp[i - 255]
# print(gf_log)
# print(gf_exp)

# gf_exp = [0] * 512  # 512个元素的列表. Python 2.6+可以考虑使用bytearray类型
# gf_log = [0] * 256
#
#
# def init_tables(prim=0x11d):
#     # 使用参数prim给的本原多项式计算指数表和对数表备用
#     global gf_exp, gf_log
#     gf_exp = [0] * 512  # anti-log (exponential指数) table
#     gf_log = [0] * 256  # log(对数) table
#     # 计算每一个GF(2^8)域内正整数的指数和对数
#     x = 1
#     for i in range(0, 255):
#         gf_exp[i] = x  # 存储指数表
#         gf_log[x] = i  # 存储对数表
#         # 更一般的情况用下面这行，不过速度较慢
#         # x = gf_mult_noLUT(x, 2, prim)
#
#         # 只用到 generator==2 或指数底为 2的情况下，用下面的代码速度快过上面的 gf_mult_noLUT():
#         x <<= 1
#         if x & 0x100:  # 等效于 x >= 256, 但要更快些 (because 0x100 == 256，位运算速度优势)
#             x ^= prim  # substract the primary polynomial to the current value (instead of 255, so that we get a unique set made of coprime numbers), this is the core of the tables generation
#
#     # Optimization: 双倍指数表大小可以省去为了不出界而取模255的运算 (因为主要用这个表来计算GF域乘法，仅此而已).
#     for i in range(255, 512):
#         gf_exp[i] = gf_exp[i - 255]
#     return [gf_log, gf_exp]
# init_tables()
# print(gf_log)
# print(gf_exp)

# def mySqrt(num):
#     t = num
#     t = 0x5fe6ec85e7de30da - (t >> 1)
#     while not (t * t <= num and (t + 1) * (t + 1) > num):
#         t = (num / t + t) / 2
#     print(float(t))
# mySqrt(2)
# print(2**0.5)
# num = 1
# for i in range(1, 55):
#     num = num*i
# print(len(str(num)))
# m = [i for i in range(1,55)]
# random.shuffle(m)
# print(m)