# coding: utf-8
import sys, getopt
import time
# opts, args = getopt.getopt(sys.argv[1:], "ho:", ["help", "output="])
# print (opts)
# print ('***************')
# print (args)
time1 = time.asctime()
print time1
time2 = time.strftime("%Y-%m-%d %H:%M:%S")
print time2
zz = time.tzname[0]
b = zz.encode('latin-1').decode('gbk')
print b
for x in zz:
    print (x)