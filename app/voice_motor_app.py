import threading
import client
import time
# from library import log
import open_jtalk

def voice_listener(response):
    if not ('direction' in response):
        open_jtalk.jtalk("あ")
        client.voice_cmd(voice_listener, 'voice_to_motor')
    else:
        open_jtalk.jtalk("ふ")
        direction = response['direction']
        # log.communication('voice_motor_app' + direction)
        client.motor_move(direction)
        time.sleep(5)
        #client.voice_cmd(voice_listener, 'voice_to_motor')


class MainThread(threading.Thread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        client.voice_cmd(voice_listener, 'voice_to_motor')
        time.sleep(4)
        # client.motor_move("right")

thread = MainThread()
client.startListener(thread)
