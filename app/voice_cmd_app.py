import threading
import client

class MainThread(threading.Thread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        client.voice_cmd()

# 実行
thread = MainThread()
client.startListener(thread)