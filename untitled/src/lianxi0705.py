# from enum import Enum, EnumMeta
#
# ccc = Enum('ddd', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
# print(type(Enum))
# print(type(ccc))
# for name, member in ccc.__members__.items():
#     print(name, '=>', member, ',', member.value)
#
#
# class Anima(Enum):
#     dog = 1
#     cat = 2
#     bee = 3
#
#
# print(Anima._member_map_.items())

import sys


def fibonacci(n):  # 生成器函数 - 斐波那契
    a, b, counter = 0, 1, 0
    while True:
        if (counter > n):
            return
        yield a
        a, b = b, a + b
        counter += 1


f = fibonacci(10)  # f 是一个迭代器，由生成器返回生成

while True:
    try:
        print(next(f))
    except StopIteration:
        sys.exit()