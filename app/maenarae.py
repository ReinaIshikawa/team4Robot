import threading
import client
import Pursuit as import pu
import time




class MainThread(threading.Thread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        pursuit=pu.MainThread()
        pursuit.run()
        print("Maenarae!")
        client.get_attack(0,90)
        print("Naore!")
        time.sleep(3)
        client.get_attack(90,0)


# 実行
thread = MainThread()
client.startListener(thread)