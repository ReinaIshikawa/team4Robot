import client
import threading
import pygame.mixer
import time
from library import log

#1.request a music jenre
#2.play a music of the jenre 


def voice_listener(response):
    if not response['music']:
        client.voice_cmd(voice_listener, 'voice_to_music')
    else:
        time.sleep(15.25)
        client.voice_cmd(voice_listener, 'voice_to_music')
    
    """
    if '嵐' in voice:
        pygame.mixer.init()
        pygame.mixer.music.load(".mp3")
        pygame.mixer.music.play(1)
        time.sleep(60)
        pygame.mixer.music.stop()

    if 'アニソン' in voice:
        pygame.mixer.init()
        pygame.mixer.music.load("zankoku.mp3")
        pygame.mixer.music.play(1)
        time.sleep(60)
        pygame.mixer.music.stop()
      
    if '洋楽' in voice:
        pygame.mixer.init()
        pygame.mixer.music.load(".mp3")
        pygame.mixer.music.play(1)
        time.sleep(60)
        pygame.mixer.music.stop()
    """




class MainThread(threading.Thread):
    def __init__(self):
        super(MainThread, self).__init__()
        
    def run(self):
        client.voice_cmd(voice_listener,'voice_to_music')

thread = MainThread()
client.startListener(thread)
