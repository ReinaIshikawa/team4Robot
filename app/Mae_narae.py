import threading
import client
import Pursuit
from Motor import servo_thread


# import json
# import sys
# from signal import signal, SIGPIPE, SIG_DFL
# signal(SIGPIPE,SIG_DFL)
# distスレッドから距離をとって，
# 近すぎたらモータースレッドにストップの指示をだすapplication

# 前ならえアプリ
# Pursuitして正面に来たらアームを床から90度動かす

def maenarae(self){
    ps=Pursuit.MainThread()
    ps.run()
    request={
        'cmd' : 'maenarae'
    }
    # se=servo_thread.ServoThread()
    # se.run()
}


class MainThread(threading.Thread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.maenarae()

# 実行
thread = MainThread()
client.startListener(thread)