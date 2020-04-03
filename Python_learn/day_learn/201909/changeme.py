# def change_me(my_list):
#     my_list.append([1,2,3,4])
#     print(my_list)
#
# my_list = [10,20,30]
# change_me(my_list)
# print(my_list)
#
#
# def ChangeInt(a):
#     m = a
#     a = 10
#     c = a
#     print(m,c)
#
#
# b = 2
# ChangeInt(b)
# print(b)

def printInfo(name,age,**var):
    print(name,age)
    for var in var:
        print(var)

printInfo(40,"Tom",set="男",data="2018-05-21")
