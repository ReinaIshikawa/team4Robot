import threading
import client
import time
# from library import log

def voice_listener(response):
    if not ('direction' in response):
        client.voice_cmd(voice_listener, 'voice_to_motor')
    else:
        direction = response['direction']
        # log.communication('voice_motor_app' + direction)
        print('voice_motor_app' + direction)
        client.motor_move(direction)
        time.sleep(5)
        client.voice_cmd(voice_listener, 'voice_to_motor')


class MainThread(threading.Thread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        client.voice_cmd(voice_listener, 'voice_to_motor')

thread = MainThread()
client.startListener(thread)
