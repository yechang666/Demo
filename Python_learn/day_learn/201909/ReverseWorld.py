# inputWorld = "who i am"
# # s = inputWorld.split(" ")
# # worlds = s[-1::-1]
# # print(worlds)
# # print(len(inputWorld))
# for i in range(len(inputWorld)-1,-1,-1):
#     print(inputWorld[i],end="")
#
import os

path = "D:\GitDemo"
f = os.listdir(path)
for i in f:

    print(i)