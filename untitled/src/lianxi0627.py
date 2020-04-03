# print(sum([10],2))
# a = 10
# b = 12
# a,b = b,a
# print(a,b)
# age = 3
# if age >3:
#     print("")
# elif age == 0:
#     print("")
# else:
#     print(age)
# a = 1
# while True:
#     print(a)
#     a = a+1
# def my_abs(x):
#     if x >= 0:
#         return x
#     else:
#         return -x
# print(my_abs(99))
# class Student(object):
#     @property
#     def score(self):
#         return self._score
#     @score.setter
#     def score(self,value):
#         self._score = value
# 
# class Screen(object):
#     @property
#     def width(self):
#         return self._width
#
#     @width.setter
#     def width(self,value1):
#         self._width=value1
#
#
#     @property
#     def height(self):
#         return self._height
#
#     @height.setter
#     def height(self,value2):
#         self._height=value2
#
#
#     @property
#     def resolution(self):
#         return self.width*self.height
# s = Screen()
# s.width = 1024
# s.height = 768
# print('resolution =', s.resolution)
# if s.resolution == 786432:
#     print('测试通过!')
# else:
#     print('测试失败!')
class Animal(object):
    print('我是动物')

# 大类:
class Mammal(Animal):
    print('哺乳动物')

class Bird(Animal):
    print('鸟类')

# 各种动物:
class Dog(Mammal):
    print('哺乳动物')

class Bat(Mammal):
    print('哺乳动物')

class Parrot(Bird):
    print('鸟类')

class Ostrich(Bird):
    print('鸟类')
class Runnable(object):
    def run(self):
        print('Running...')

class Flyable(object):
    def fly(self):
        print('Flying...')

class Dog(Mammal, Runnable):
    pass
class Bat(Mammal, Flyable):
    pass
