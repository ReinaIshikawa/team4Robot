import client
import threading
# import pygame.mixer
import time
# from library import log

#1.request a music jenre
#2.play a music of the jenre


def voice_listener(response):
    # Nothing can be printed here... But it maybe works
    # print('hey music!')
    if not ('music' in response):
        client.voice_cmd(voice_listener, 'voice_to_music')
        # print('no music')
    else:
        # print('music app received ', response['music'])
        # words of songs can be orders?
        time.sleep(8.25)
        #client.motor_move("rotate")
        client.voice_cmd(voice_listener, 'voice_to_music')

class MainThread(threading.Thread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        client.voice_cmd(voice_listener,'voice_to_music')

thread = MainThread()
client.startListener(thread)
