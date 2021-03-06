from . import client
import threading
import pygame.mixer
import time

#1.request an artist name
#2.play music which the artist sings


def voice_listener(response):
    voice = response['voice']
    if 'ろっく' in voice:
        pygame.mixer.init()
        pygame.mixer.music.load(".mp3")
        pygame.mixer.music.play(1)
        time.sleep(60)
        pygame.mixer.music.stop()

    if 'あにそん' in voice:
        pygame.mixer.init()
        pygame.mixer.music.load("zankoku.mp3")
        pygame.mixer.music.play(1)
        time.sleep(60)
        pygame.mixer.music.stop()

"""        
    if 'ようがく' in voice:
        pygame.mixer.init()
        pygame.mixer.music.load(".mp3")
        pygame.mixer.music.play(1)
        time.sleep(60)
        pygame.mixer.music.stop()

    client.get_voice(voice_listener)
"""

class MainThread(threading.Thread):
    def __init__(self):
        super(MainThread, self).__init__()
        
    def run(self):
        client.get_voice(voice_listener)

thread = MainThread()
client.startListener(thread)
