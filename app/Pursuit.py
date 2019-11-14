import threading
import client
from client import log

# import json
# import sys
# from signal import signal, SIGPIPE, SIG_DFL
# signal(SIGPIPE,SIG_DFL)
# distスレッドから距離をとって，
# 近すぎたらモータースレッドにストップの指示をだすapplication

# callback関数
# responseはdistからのresponseが入る

def pursuit_listener1(response):
    # メインモータースレッドに距離を渡す
    # 速度は向こうで制御してくれる
    dist = response['dist']
    log.communication("pursuit dist"+dist)
    if dist!=0:
        client.motor_dist_check(dist)
    # 再帰的に(繰り返し)処理をするため
    # runの方にwhile文で書いてもいいかも
        client.get_dist(pursuit_listener1)
        

def pursuit_listener2(response):
    x = response['x']
    y = response['y']
    log.communication("pursuit angle"+x+", "+y)
    if x>0:
        client.motor_angle_check(x,y)
    # 再帰的に(繰り返し)処理をするため
    # runの方にwhile文で書いてもいいかも
        client.get_angle(pursuit_listener2)
    else:
        client.get_dist(pursuit_listener1)



class MainThread(threading.Thread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        client.get_angle(pursuit_listener2)


# 実行
thread = MainThread()
client.startListener(thread)


