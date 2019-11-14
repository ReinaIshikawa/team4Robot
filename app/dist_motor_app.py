import threading
import client

# import json
# import sys
# from signal import signal, SIGPIPE, SIG_DFL
# signal(SIGPIPE,SIG_DFL)
# distスレッドから距離をとって，
# 近すぎたらモータースレッドにストップの指示をだすapplication

# callback関数
# responseはdistからのresponseが入る

def dist_listener(response):
    # メインモータースレッドに距離を渡す
    # 速度は向こうで制御してくれる
    dist = response['dist']
    client.motor_dist_check(dist)
    # 再帰的に(繰り返し)処理をするため
    # runの方にwhile文で書いてもいいかも
    client.get_dist(dist_listener)


class MainThread(threading.Thread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        client.get_dist(dist_listener)
        client.get_dist(dist_)


# 実行
thread = MainThread()
client.startListener(thread)

# 1. applicationのMainthreadのインスタンスが生成，
# client.pyのstartListener関数の引数として渡される
# 2. Mainthreadのrun()が実行される
# 3. run()ではまずget_distが実行され
# 4. callback関数としてdist_lisnerがセットされる
# 5. distからresponseがくると，client.pyのLisnerの'sensor'リストにcallbackが入る
# 6. リストに入ってきた順にcallbackを実行していく
