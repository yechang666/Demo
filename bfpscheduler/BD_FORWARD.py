# -*- coding: utf -8 -*-
# @Time     :2019/12/31 11:56
# @Author   :lzw
# @Email    :601923086@qq.com
# @File     :BD_FORWARD.py
import threading
import time
import os
import queue
import socket
import signal
import sys

msgQ = queue.Queue()
mtx = threading.Lock()
semaphore = threading.Semaphore(0)

recvLen = 0
sendLen = 0


## thread receiver
def bdRecv():
    HOST = '192.168.10.190'
    PORT = 55102
    # s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)


    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        print("loop start")
        try:
            print("try to connect socket")

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            print("********************connect server ok...")
            while 1:
                try:
                    global recvLen
                    global mtx
                    global semaphore

                    data = s.recv(20480)
                    print("get data ok")

                    if len(data) == 0:
                        print("Get none data, break")
                        break

                    mtx.acquire()  # wait mutex until released
                    msgQ.put(data)
                    mtx.release()
                    semaphore.release()

                    # recvLen = recvLen + bytes(data).len()
                    print("thread received data: %s" % data)


                    continue
                except socket.error as e:
                    print("recv error data, maybe connection lost")
                    break
        except:
            # print('retry...')
            time.sleep(5)
            continue

            # s.connect((HOST,PORT))
            # mtx.release()

            # print "********************connect server ok..."
            # while 1:
            # cmd=raw_input("Please input cmd:")
            # s.sendall(cmd)
            #	global recvLen
            #	global mtx
            #		global semaphore

            #	data=s.recv(2048)
            #	print "get data ok"
            #	mtx.acquire() # wait mutex until released
            #	msgQ.put(data)
            #	mtx.release()
            #	semaphore.release()

            # recvLen = recvLen + bytes(data).len()
    # print "thread received data: %s" %data

        s.close()


## thread sender
def fesSender():
    HOST = '192.168.10.26'
    PORT = 20088
    # s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # s.connect((HOST,PORT))

    # while 1:
    #	global sendLen
    #	global mtx
    #	global semaphore

    #	semaphore.acquire()

    #	mtx.acquire() # wait mutex until released
    #	data = msgQ.get()
    #	mtx.release()

    #	#print "recv bytes: %s" %(str(data,'utf8'))
    #	s.sendall(data)
    #	#sendLen = sendLen + bytes(data).len()

    while True:

        try:
            print("try to connect forwarder socket")

            # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # s.connect((HOST,PORT))

            while 1:
                try:
                    global recvLen
                    global mtx
                    global semaphore

                    semaphore.acquire()

                    mtx.acquire()  # wait mutex until released
                    data = msgQ.get()
                    mtx.release()

                    # s.sendall(data)
                    udp_socket.sendto(data, (HOST, PORT))

                    continue
                except socket.error as e:
                    print("recv error data, maybe forwarder connection lost")

                    break
        except:
            # print('retry...')
            time.sleep(5)
            continue

        udp_socket.close()


recvThread = threading.Thread(target=bdRecv)
sendThread = threading.Thread(target=fesSender)


def exit(signum, frame):
    print('Ctrl+C! DONE.')
    # sendThread.terminate()
    # recvThread.terminate()
    sys.exit()


signal.signal(signal.SIGINT, exit)
signal.signal(signal.SIGTERM, exit)

for t in [recvThread, sendThread]:
    t.setDaemon(True)
    t.start()

while 1:
    time.sleep(10)
    print("Recv bytes: %d; Send Bytes: %d" % (recvLen, sendLen))




