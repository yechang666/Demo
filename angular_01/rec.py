# @Time     :2019/12/23 16:41
# @Author   :lzw
# @Email    :601923086@qq.com
# @File     :rec.py

import socket
import time
import struct

PORT = 20088
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = ("192.168.10.26", PORT)
receiver_socket.bind(address)

while True:
        now = time.time()
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now)))
        receive_message, client = receiver_socket.recvfrom(1024)
        data = struct.unpack('<2d1b',receive_message)
        # print ('num1:' ,data[0], ' num2:',data[1], ' num3:',data[2])
        print(data)