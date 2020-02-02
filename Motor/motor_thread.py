# import requests
import json
import sys
import time
import wiringpi as wp
import struct
from .Motor_move import Motor_move
import threading

# Processは使わず，threadのみで完結させる
# Motor_MoveはMotorを継承

class MotorThread(threading.Thread):
    def __init__(self, app):
        super(MotorThread, self).__init__()
        self.speed = 20000
        self.app = app
        self.right = Motor_move(0, self.speed)
        self.left = Motor_move(1, self.speed)
        self.cnt = 0


    def SimpleMove(self,direction):
        print("in simple move: ", direction)
        if direction == 'front':
            self.right.Run_forward()
            self.left.Run_forward()
        elif direction == 'back':
            self.right.Run_back()
            self.left.Run_back()
        elif direction == 'right':
            self.right.Turn_right()
            self.left.Turn_right()
        elif direction == 'left':
            self.right.Turn_left()
            self.left.Turn_left()
        elif direction == 'stop':
            self.right.Softstop()
            self.left.Softstop()
            self.right.Softhiz()
            self.left.Softhiz()
        elif direction == 'stay':
            pass

    def run(self, request=None):
        if not request:
            return
        print('motor_thread->motor: {}:{}'.format(self.cnt, request))
        self.cnt += 1
        if (request['cmd'] == 'check_dist'):
            self.right.PID(request['dist'])
            self.left.PID(request['dist'])
        elif (request['cmd'] == 'check_angle'):
            self.right.Angle(request['x'], request['y'])
            self.left.Angle(request['x'], request['y'])
        elif (request['cmd'] == 'move'):
            print("checknow:",request['direction'])
            print("type:",type(request['direction']))
            self.SimpleMove(request['direction'])
