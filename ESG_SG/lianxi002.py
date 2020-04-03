#
import math


# X = math.pi
#
#
# def my_circle1(b):
#     sum1 = X * b * b
#     return sum1
#
#
# print my_circle1(2)


# def func(a, b, c=0, *args1, **kw):
#     print 'a =', a, 'b =', b, 'c =', c, 'args =', args1, 'kw =', kw
#
#
# args1 = (1, 2, 3, 4)
# kw = {'x': 99}
# func(*args1, **kw)


# def fact(n):
#     return fact_iter(n, 1)
#
#
# def fact_iter(num, product):
#     if num == 1:
#         return product
#     return fact_iter(num - 1, num * product)
#
#
# print fact(10)
# f = abs()

#
# def add(x, y, f):
#     return f(x) + f(y)
#
#
# print (add(3, 4, abs))
# def f(x):
#     return x * x
#
#
# a = map(f, [1, 2, 3, 4, 5, 6, 7, 8])
# print list(a)
#

# def not_empty(s):
#     # print s.strip()
#     print s and s.strip()
#     return s and s.strip()
#
#
# print list(filter(not_empty, ['A', '', 'B', None, 'C', '  ']))
# from operator import itemgetter
#
# L = ['bob', 'about', 'Zoo', 'Credit']
#
# print(sorted(L))
# print(sorted(L, key=str.lower))
#
# students = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]
#
# print(sorted(students, key=itemgetter(0)))
# print(sorted(students, key=lambda t: t[1], reverse=True))
# print(sorted(students, key=itemgetter(1), reverse=True))
# print(sorted(students, key=itemgetter(1), reverse=False))
# def count():
#     fs = []
#     for i in range(1, 4):
#         def f():
#              return i*i
#         fs.append(f)
#     return fs
#
# # f1, f2, f3 = count()
# f1 = count()
# print f1[0]()
# # print count()
# for a in count():
#     print a()
#
# str1 = "14659  2  16% S   129 1076352K  60388K  fg u0_a14   cn.com.gvmedia.silkwave.csserver"
# l= str1.split()
#
#
# def getitems(a, *key):
#     if isinstance(a, str):
#         res = ''.join(map(lambda i: a[i], key))
#     else:
#         res = type(a)(map(lambda i: a[i], key))
#     return res
#
# print getitems(l,2)
import re;
s = "7e8abafe7fd8deb68d922547342f2ef3b69f78ed1d25b53ff532ef22e7144fe8"
patt1 = "([^-]{2})"
print re.match(patt1,s).groups()



