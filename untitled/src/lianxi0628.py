# class Student(object):
#     def __init__(self, name):
#          self.name = name
#     def __str__(self):
#          return 'Student object (name: %s)' % self.name
# print(Student('Jack'))

# class Fib(object):
#     def __init__(self):
#         self.a, self.b = 0, 1 # 初始化两个计数器a，b
#
#     def __iter__(self):
#         return self # 实例本身就是迭代对象，故返回自己
#
#     def __next__(self):
#         self.a, self.b = self.b, self.a + self.b # 计算下一个值
#         if self.a > 1000: # 退出循环的条件
#             raise StopIteration()
#         return self.a # 返回下一个值
# for n in Fib():
#      print(n)
# print((n for n in Fib()))
# from enum import Enum
#
# Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
# for name, member in Month._member_map_.items():
#     print(name, '=>', member, ',', member.value)
# #
#
# def bar(s):
#     pass
#
#
# try:
#     (bar(2))
# except Exception as e:
#     print("",e)
# finally:
#     print()
# import builtins
# print(len(dir(builtins)))
# for n in dir(builtins):
#     print(n)

# from enum import Enum
# Month = Enum('Month','Jan Feb Mar')
# Month._member_map_.items()
# print(type(Enum))
# print(type(Month))
# def ccc():
#     foo('0')
#
# def foo(s):
#     print('进入函数')
#     n = int(s)
#     assert n != 0, 'n is zero!'
#     return 10 / n
# ccc()
#
# import logging
# logging.basicConfig(level=logging.INFO)
# s = '0'
# n = int(s)
# logging.info('n = %d' % n)
# print(10 / n)
import unittest
# from mydict import MyDict
# class Dict(dict):
#
#     def __init__(self, **kw):
#         super().__init__(**kw)
#
#     def __getattr__(self, key):
#         try:
#             return self[key]
#         except KeyError:
#             raise AttributeError(r"'Dict' object has no attribute '%s'" % key)
#
#     def __setattr__(self, key, value):
#         self[key] = value
# class TestDict(unittest.TestCase):
#
#     def test_init(self):
#         d = Dict(a=1, b='test')
#         self.assertEqual(d.a, 1)
#         self.assertEqual(d.b, 'test')
#         self.assertTrue(isinstance(d, dict))
#
#     def test_key(self):
#         d = Dict()
#         d['key'] = 'value'
#         self.assertEqual(d.key, 'value')
#
#     def test_attr(self):
#         d = Dict()
#         d.key = 'value'
#         self.assertTrue('key' in d)
#         self.assertEqual(d['key'], 'value')
#
#     def test_keyerror(self):
#         d = Dict()
#         with self.assertRaises(KeyError):
#             value = d['empty']
#
#     def test_attrerror(self):
#         d = Dict()
#         with self.assertRaises(AttributeError):
#             value = d.empty
#
# if __name__ == '__main__':
#     unittest.main()
# import osed a child process (%s).' % (os.getpid(), pid))
# print('Process (%s) start...' % os.getpid())
# # Only works on Unix/Linux/Mac:
# pid = os.fork()
# if pid == 0:
#     print('I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid()))
# else:
#     print('I (%s) just creat

# from multiprocessing import Pool
# import os, time, random
#
# def long_time_task(name):
#     print('Run task %s (%s)...' % (name, os.getpid()))
#     start = time.time()
#     time.sleep(random.random() * 3)
#     end = time.time()
#     print('Task %s runs %0.2f seconds.' % (name, (end - start)))
#
# if __name__=='__main__':
#     print('Parent process %s.' % os.getpid())
#     p = Pool(10)
#     for i in range(20):
#         p.apply_async(long_time_task, args=(i,))
#     print('Waiting for all subprocesses done...')
#     p.close()
#     p.join()
#     print('All subprocesses done.')

# import subprocess
#
# print('$ nslookup www.python.org')
# r = subprocess.call(['nslookup', 'www.python.org'])
# print('Exit code:', r)

# import time, threading
#
# # 新线程执行的代码:
# def loop():
#     print('thread %s is running...' % threading.current_thread().name)
#     n = 0
#     while n < 5:
#         n = n + 1
#         print('thread %s >>> %s' % (threading.current_thread().name, n))
#         time.sleep(1)
#     print('thread %s ended.' % threading.current_thread().name)
#
# print('thread %s is running...' % threading.current_thread().name)
# t = threading.Thread(target=loop, name='LoopThread')
# t.start()
# t.join()
# print('thread %s ended.' % threading.current_thread().name)

# from turtle import *
#
# def drawStar(x, y):
#     pu()
#     goto(x, y)
#     pd()
#     # set heading: 0
#     seth(0)
#     for i in range(5):
#         fd(40)
#         rt(144)
#
# for x in range(0, 250, 50):
#     drawStar(x, 0)
#
# done()

# from turtle import *
#
# # 设置色彩模式是RGB:
# colormode(255)
#
# lt(90)
#
# lv = 14
# l = 120
# s = 45
#
# width(lv)
#
# # 初始化RGB颜色:
# r = 0
# g = 0
# b = 0
# pencolor(r, g, b)
#
# penup()
# bk(l)
# pendown()
# fd(l)
#
# def draw_tree(l, level):
#     global r, g, b
#     # save the current pen width
#     w = width()
#
#     # narrow the pen width
#     width(w * 3.0 / 4.0)
#     # set color:
#     r = r + 1
#     g = g + 2
#     b = b + 3
#     pencolor(r % 200, g % 200, b % 200)
#
#     l = 3.0 / 4.0 * l
#
#     lt(s)
#     fd(l)
#
#     if level < lv:
#         draw_tree(l, level + 1)
#     bk(l)
#     rt(2 * s)
#     fd(l)
#
#     if level < lv:
#         draw_tree(l, level + 1)
#     bk(l)
#     lt(s)
#
#     # restore the previous pen width
#     width(w)
#
# speed("fastest")
#
# draw_tree(l, 4)
#
# done()

class A():
    def add(self,a,b):
        return a + b
class B(A):
    def sub(self,a,b):
        return a - b

count = B()
c = count.add(3,6)
print(c)