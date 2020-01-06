import threading
import client

def face_listener(response):
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