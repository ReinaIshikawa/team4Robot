import client
import threading
import pygame.mixer
import time
from library import log

#1.request an artist name
#2.play music which the artist sings


def voice_listener(response):
    voice = response['voice']
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
        client.get_voice(voice_listener)

thread = MainThread()
client.startListener(thread)
