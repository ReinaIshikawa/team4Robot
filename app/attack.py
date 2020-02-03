import threading
import client
import time
# import Pursuit 対象まで移動するアプリ
# import json
# import sys
# from signal import signal, SIGPIPE, SIG_DFL
# signal(SIGPIPE,SIG_DFL)
# 対象の物体まで進むmoveアプリを呼び出す
# その後剣（サーボモーター）を振る

# def dist_listener():
#     client.get_attack(20,160)

def pursuit_listener1(response):
    global count
    # メインモータースレッドに距離を渡す
    # 速度は向こうで制御してくれる
    dist = response['dist']
    #print("pursuit dist"+str(dist))
    if dist!=0:
        client.motor_dist_check(dist)
        client.get_dist(pursuit_listener1)
    else:
        client.motor_move("stop")
        time.sleep(1)
        for i in range(10):
            client.get_attack(20, 160)
            time.sleep(2)
        client.get_angle(pursuit_listener2)
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
        self.start_dig = 20
        self.end_dig = 160

    def run(self):
        client.get_angle(pursuit_listener2)
        

# 実行
thread = MainThread()
client.startListener(thread)
