import requests
import json
import sys
import time
import wiringpi as wp
import struct
from Motor import Motor
import Motor_move as Mmove

class MotorThread(threading.Thread):
	def _init_(self, request, motor):
		super(MotorThread, self)._init_()
		self.request = request
		self.motor = motor
		self.speed = 20000

	def run(self):
		right = Motor_move(0, speed)
		left=Motor_move(1,speed)

		while True:
			if self.request['cmd'] == 'front':
				right.Run_forward()
				left.Run_forward()
				time.sleep(1)

			elif self.request['cmd'] == 'back':
				right.Run_back()
				left.Run_back()
				time.sleep(1)

			elif self.request['cmd'] == 'right':
				right.Turn_right()
				left.Turn_right()
				time.sleep(1)

			elif self.request['cmd'] == 'left':
				right.Turn_left()
				left.Turn_left()
				time.sleep(1)

			elif self.request['cmd'] == 'stop':
				right.Softstop()
				left.Softstop()
				right.Softhiz()
				left.Softhiz()
				self.request['cmd'] = 'stay':

			elif self.request['cmd'] == 'stay':
				continue
