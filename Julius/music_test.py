import time
import pygame.mixer

pygame.mixer.init()
pygame.mixer.music.load("../Julius/zankoku.mp3")
pygame.mixer.music.play(1)
time.sleep(15)
pygame.mixer.music.stop()
