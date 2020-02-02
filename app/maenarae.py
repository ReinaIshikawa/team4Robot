import threading
import client
import time
import open_jtalk


def pursuit_listener1(response):
    # メインモータースレッドに距離を渡す
    # 速度は向こうで制御してくれる
    dist = response['dist']
    #print("pursuit dist"+str(dist))
    #if dist!=0:
        ##client.motor_dist_check(dist)
        #client.get_dist(pursuit_listener1)
    if True:
        client.motor_move("stop")
        open_jtalk.jtalk("まえならえ")
        #print("Maenarae!")
        client.get_attack(0,90)
        time.sleep(3)
        open_jtalk.jtalk("なおれ")
        #time.sleep(3)
        client.get_attack(90,0)
        #client.get_angle(pursuit_listener2)
        #print(count)


def pursuit_listener2(response):
    open_jtalk.jtalk("い")
    x = response['x']
    y = response['y']
    # log.communication("pursuit angle"+str(x)+", "+str(y))
    #print("pursuit angle"+str(x)+", "+str(y))
    time.sleep(1)
    if x<0:# no human
        client.get_dist(pursuit_listener1)
        client.motor_angle_check(10,y)
        #client.get_angle(pursuit_listener2)
    elif (x<200 or x>400):
        client.motor_angle_check(x, y)
        #client.get_angle(pursuit_listener2)
        client.get_dist(pursuit_listener1)
    else:
        client.get_dist(pursuit_listener1)

        
class MainThread(threading.Thread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        open_jtalk.jtalk("いち")
        client.get_angle(pursuit_listener2)
        open_jtalk.jtalk("に")
        time.sleep(20)



# 実行
thread = MainThread()
client.startListener(thread)
