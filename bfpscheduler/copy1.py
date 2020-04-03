# dd = {
#     "a":123,
#     "b":[{
#         "c":456,
#         "d":"jjj"
#     }]
# }
#
# dd['b']["d"] = 888
# print(dd)
# # print(cc)
# aa = [135,235,654]
# print('135' in str(aa))
# print(type(aa))
# print(type(str(aa)))
# while True:
#     x = input('Input an integer: ')
#     if x.isdigit():
#         break
#     else:
#         print ('Please input an *integer*')

# for a in 123456:
#     if ord(a)>=75 or ord(a)<=48:
#         print('包含非法字符')
# for i in range(256):
#     print(chr(i),end='\t')
import time
# count = 0
time1 = time.time()
# while True:
#     if count > 2**30:
#         break
#     count +=1
# time2 = time.time()
# diff_time = time2 - time1
# print(diff_time)
for i in range(10):
    pass
time2 = time.time()
diff_time = time2 - time1
print(diff_time)