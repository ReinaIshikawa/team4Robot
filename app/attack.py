import threading
import client
import time
# import move_to_target as mtt# 対象まで移動するアプリ
# import json
# import sys
# from signal import signal, SIGPIPE, SIG_DFL
# signal(SIGPIPE,SIG_DFL)
# 対象の物体まで進むmoveアプリを呼び出す
# その後剣（サーボモーター）を振る

# def dist_listener():
#     client.get_attack(20,160)


class MainThread(threading.Thread):
    def __init__(self):
        super(MainThread, self).__init__()
        self.start_dig = 20
        self.end_dig = 160

    def run(self):
        # client.get_move_to_target(mtt.move_to_target_listener)
        for i in range(10):
            client.get_attack(self.start_dig, self.end_dig)
            self.start_dig = self.end_dig + 5
            self.end_dig = self.end_dig - 5
            time.sleep(2)


# 実行
thread = MainThread()
client.startListener(thread)