# list1 = ['Google', 'Runoob', 1997, 2000]
# # dd = list1[0]
# # print(dd)
# list2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# # x = [list1,list2]
# # for i in x:
# #     for j in i:
# #         print(j)
#
#
# # seq = (1,2,3,4,5,6)
# # print(list(seq))
# # print(tuple(list2))
# dd = list2.reverse()
# print(dd)

for i in range(1, 10):
    for j in range(1, i+1):
        print('{}x{}={}\t'.format(j, i, i*j), end='')
    print()