import threading
import client
import time
# from library import log

# import json
# import sys
# from signal import signal, SIGPIPE, SIG_DFL
# signal(SIGPIPE,SIG_DFL)
# distスレッドから距離をとって，
# 近すぎたらモータースレッドにストップの指示をだすapplication

# callback関数
# responseはdistからのresponseが入る
count=0
def pursuit_listener1(response):
    global count
    # メインモータースレッドに距離を渡す
    # 速度は向こうで制御してくれる
    dist = response['dist']
    #print("pursuit dist"+str(dist))
    if dist!=0:
        client.motor_dist_check(dist)
        client.get_dist(pursuit_listener1)
    elif count <=10:
        client.motor_move("stop")
        time.sleep(1)
        client.get_angle(pursuit_listener2)
        count+=1
        #print(count)

def pursuit_listener2(response):
    x = response['x']
    y = response['y']
    # log.communication("pursuit angle"+str(x)+", "+str(y))
    #print("pursuit angle"+str(x)+", "+str(y))
    if x<0:
        client.get_dist(pursuit_listener1)
    elif (x<200 or x>400):
        client.get_angle(pursuit_listener2)
    else:
        client.get_dist(pursuit_listener1)



class MainThread(threading.Thread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        time.sleep(3)
        client.get_angle(pursuit_listener2)


# 実行
thread = MainThread()
client.startListener(thread)
