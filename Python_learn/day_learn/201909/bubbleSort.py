# aa = [9,2,5,3,8,1]
import random

def bubbleSort(aa):
    for i in range(len(aa)-1):
        for i in range(len(aa)-1):
            if aa[i]>aa[i+1]:
                aa[i],aa[i+1] = aa[i+1],aa[i]
    return aa

dd = []
for i in range(30):
    cc = random.randint(10,50)
    dd.append(cc)
print(dd)
bubbleSort(dd)
print(dd)
