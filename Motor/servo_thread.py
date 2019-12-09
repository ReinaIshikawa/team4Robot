#!/usr/bin/env python
# -*- coding: utf-8 -*-
import  Adafruit_PCA9685
import time
import sys
import json
import servo

class ServoThread(threading.Thread):
	def __init__(self, request, servo, app):
		super(ServoThread, self).__init__()
		self.request = request
		self.servo = servo
		self.app = app
		

	def run(self):
		servo0 = servo.servo_Class(Channel=0, ZeroOffset=-5)
		servo1 = servo.servo_Class(Channel=1, ZeroOffset=-5)
		# servo2 = servo.servo_Class(Channel=2, ZeroOffset=-5)

		while True:
			#縦に動かす
			if self.request['cmd'] == 'clean':
				servo0.rotate(45, 90)
				time.sleep(1)

			#横に動かす
			if self.request['cmd'] == 'attack':
				servo1.rotate(45, 90)
				time.sleep(1)
				
			#止める
			if self.request['cmd'] == 'quit':
				servo0.rotate(-1, -1)
				servo1.rotate(-1, -1)
				time.sleep(1)
				



