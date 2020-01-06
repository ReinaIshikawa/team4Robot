import threading
import client
import move_to_target as mtt# 対象まで移動するアプリ
# import json
# import sys
# from signal import signal, SIGPIPE, SIG_DFL
# signal(SIGPIPE,SIG_DFL)
# 対象の物体まで進むmoveアプリを呼び出す
# その後剣（サーボモーター）を振る


class MainThread(threading.Thread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        # client.get_move_to_target(mtt.move_to_target_listener)
        client.get_attack(20,160)


# 実行
thread = MainThread()
client.startListener(thread)